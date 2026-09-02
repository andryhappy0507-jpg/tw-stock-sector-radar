from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


ROBOTICS_SUBTHEMES = [
    "ROBOT_BODY_PLATFORM",
    "ROBOT_CONTROL_SYSTEM",
    "ROBOT_EDGE_AI",
    "ROBOT_AMR",
    "ROBOT_SYSTEM_INTEGRATION",
    "ROBOT_TRANSMISSION",
    "ROBOT_ACTUATION",
    "ROBOT_END_EFFECTOR",
    "ROBOT_VISION",
]

NEW_ROBOTICS_SUBTHEMES = [
    theme_id for theme_id in ROBOTICS_SUBTHEMES if theme_id != "ROBOT_VISION"
]

FORMAL_ROBOTICS_POOL_THEMES = ["ROBOTICS", "ROBOT_COMPONENTS", "ROBOT_VISION"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the approved robotics subtheme weekly signal report."
    )
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/research"))
    parser.add_argument("--output-file", type=Path)
    parser.add_argument("--run-number", default="")
    parser.add_argument("--head-sha", default="")
    return parser.parse_args()


def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return pd.read_csv(path, dtype={"stock_id": str}).fillna("")


def bool_value(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin(["true", "1", "yes"])


def fmt_pct(value: object, digits: int = 1) -> str:
    if value == "" or pd.isna(value):
        return "—"
    return f"{float(value):.{digits}f}%"


def main() -> None:
    args = parse_args()
    data_dir = args.data_dir.resolve()
    output_dir = args.output_dir.resolve()

    weekly = load_csv(data_dir / "weekly_signal.csv")
    summary = load_csv(data_dir / "theme_signal_summary.csv")
    group_summary = load_csv(data_dir / "theme_group_signal_summary.csv")
    mapping = load_csv(data_dir / "stock_theme_map.csv")
    themes = load_csv(data_dir / "theme_master.csv")
    weekly_summary = load_csv(data_dir / "weekly_summary.csv")

    if weekly_summary.empty:
        raise ValueError("weekly_summary.csv has no rows")
    latest_date = str(weekly_summary.iloc[0]["latest_date"])
    previous_date = str(weekly_summary.iloc[0]["previous_week_date"])

    approved = mapping.loc[
        mapping["status"].eq("active")
        & mapping["approval_status"].isin(["approved", "auto_approved"])
    ].copy()
    detail_map = approved.loc[approved["theme_id"].isin(ROBOTICS_SUBTHEMES)].copy()

    theme_names = themes.set_index("theme_id")["theme_name"].to_dict()
    detail = summary.loc[summary["theme_id"].isin(ROBOTICS_SUBTHEMES)].copy()
    missing = set(ROBOTICS_SUBTHEMES) - set(detail["theme_id"])
    if missing:
        raise ValueError(f"Theme summary is missing robotics subthemes: {sorted(missing)}")

    numeric_cols = [
        "mapped_stock_count",
        "avg_weekly_return_pct",
        "up_ratio",
        "price_strong_count",
        "volume_strong_count",
        "A_count",
        "B_count",
        "C_count",
    ]
    for col in numeric_cols:
        detail[col] = pd.to_numeric(detail[col], errors="coerce")

    weekly_join = detail_map.merge(weekly, on="stock_id", how="left")
    weekly_join["weekly_return_pct"] = pd.to_numeric(
        weekly_join["weekly_return_pct"], errors="coerce"
    )
    weekly_join["price_strong_bool"] = bool_value(weekly_join["price_strong"])
    weekly_join["volume_strong_bool"] = bool_value(weekly_join["volume_strong"])
    name_col = "stock_name_x" if "stock_name_x" in weekly_join.columns else "stock_name"

    leader_rows = []
    for theme_id, group in weekly_join.groupby("theme_id"):
        ranked = group.dropna(subset=["weekly_return_pct"]).sort_values(
            ["weekly_return_pct", "turnover_ntd"], ascending=[False, False]
        )
        if ranked.empty:
            continue
        leader = ranked.iloc[0]
        leader_rows.append(
            {
                "theme_id": theme_id,
                "leader_stock_id": leader["stock_id"],
                "leader_stock_name": leader.get(name_col, ""),
                "leader_weekly_return_pct": leader["weekly_return_pct"],
                "leader_abc_group": leader.get("abc_group", ""),
            }
        )
    leaders = pd.DataFrame(leader_rows)
    detail = detail.merge(leaders, on="theme_id", how="left")

    detail["weekly_signal_status"] = "WATCH"
    detail.loc[
        (detail["price_strong_count"] >= 3) & (detail["up_ratio"] >= 0.60),
        "weekly_signal_status",
    ] = "PASS"
    detail["up_ratio_pct"] = detail["up_ratio"] * 100
    detail["rank"] = detail["avg_weekly_return_pct"].rank(
        method="first", ascending=False
    ).astype(int)
    detail = detail.sort_values("rank")

    formal_pool_stock_count = approved.loc[
        approved["theme_id"].isin(FORMAL_ROBOTICS_POOL_THEMES), "stock_id"
    ].nunique()
    detailed_stock_count = detail_map["stock_id"].nunique()
    detailed_mapping_count = len(detail_map)
    new_detail_map = approved.loc[
        approved["theme_id"].isin(NEW_ROBOTICS_SUBTHEMES)
    ]
    new_detailed_stock_count = new_detail_map["stock_id"].nunique()
    new_detailed_mapping_count = len(new_detail_map)

    robotics_group = group_summary.loc[group_summary["group_id"].eq("ROBOTICS_CHAIN")]
    if robotics_group.empty:
        raise ValueError("ROBOTICS_CHAIN is missing from theme_group_signal_summary.csv")
    robotics_group = robotics_group.iloc[0]

    stock_pool = approved.loc[
        approved["theme_id"].isin(FORMAL_ROBOTICS_POOL_THEMES), ["stock_id"]
    ]
    stock_pool = stock_pool.drop_duplicates().merge(weekly, on="stock_id", how="left")
    stock_pool["weekly_return_pct"] = pd.to_numeric(
        stock_pool["weekly_return_pct"], errors="coerce"
    )
    stock_pool = stock_pool.sort_values("weekly_return_pct", ascending=False)
    top_stocks = stock_pool.head(10)
    top_name_col = "stock_name_x" if "stock_name_x" in top_stocks.columns else "stock_name"

    run_text = f"GitHub Actions #{args.run_number}" if args.run_number else "GitHub Actions artifact"
    if args.head_sha:
        run_text += f"（{args.head_sha[:7]}）"

    lines = [
        f"# 機器人細分產業週報（{latest_date}）",
        "",
        f"- 資料來源：{run_text}",
        f"- 本週基準日：{latest_date}；前週基準日：{previous_date}",
        f"- 正式核准機器人池：{formal_pool_stock_count} 檔上市／上櫃股票",
        (
            f"- 本輪新核准 8 個細分 Theme：{new_detailed_stock_count} 檔、"
            f"{new_detailed_mapping_count} 筆對應"
        ),
        (
            f"- 本報告含既有機器人視覺共 9 個細分 Theme：{detailed_stock_count} 檔、"
            f"{detailed_mapping_count} 筆對應"
        ),
        "- 興櫃 7942 東佑達仍只列研究觀察，不納入正式週訊號。",
        "",
        "## 本週結論",
        "",
    ]

    passed = detail.loc[detail["weekly_signal_status"].eq("PASS")]
    if passed.empty:
        lines.append("本週沒有細分 Theme 通過同步轉強門檻。")
    else:
        pass_names = "、".join(passed["theme_name"].astype(str))
        lines.append(f"本週通過同步轉強門檻的細分 Theme：{pass_names}。")
    lines.extend(
        [
            "",
            (
                f"機器人族群聚合口徑共 {int(robotics_group['mapped_stock_count'])} 檔，"
                f"平均週報酬 {fmt_pct(robotics_group['avg_weekly_return_pct'])}，"
                f"上漲家數比 {fmt_pct(float(robotics_group['up_ratio']) * 100)}。"
            ),
            "",
            "> 週訊號 PASS 只表示本週價量同步性達標，不代表新增或核准概念股資格；概念股資格仍以人工證據審核為準。",
            "",
            "## 細分 Theme 強弱",
            "",
            "| 排名 | 細分 Theme | 週訊號 | 平均週報酬 | 上漲比 | 價強檔 | 量強檔 | 領先股 | 領先股週報酬 |",
            "|---:|---|---|---:|---:|---:|---:|---|---:|",
        ]
    )
    for _, row in detail.iterrows():
        leader = f"{row['leader_stock_id']} {row['leader_stock_name']}"
        lines.append(
            "| "
            + " | ".join(
                [
                    str(int(row["rank"])),
                    str(row["theme_name"]),
                    str(row["weekly_signal_status"]),
                    fmt_pct(row["avg_weekly_return_pct"]),
                    fmt_pct(row["up_ratio_pct"]),
                    str(int(row["price_strong_count"])),
                    str(int(row["volume_strong_count"])),
                    leader,
                    fmt_pct(row["leader_weekly_return_pct"]),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## 核心池本週領先股",
            "",
            "| 排名 | 股票 | 週報酬 | 價強 | 量強 | A/B/C |",
            "|---:|---|---:|---|---|---|",
        ]
    )
    for rank, (_, row) in enumerate(top_stocks.iterrows(), start=1):
        lines.append(
            f"| {rank} | {row['stock_id']} {row.get(top_name_col, '')} | "
            f"{fmt_pct(row['weekly_return_pct'])} | "
            f"{'是' if str(row.get('price_strong', '')).lower() == 'true' else '否'} | "
            f"{'是' if str(row.get('volume_strong', '')).lower() == 'true' else '否'} | "
            f"{row.get('abc_group', '') or '—'} |"
        )

    lines.extend(
        [
            "",
            "## 判讀規則",
            "",
            "- 個股週漲幅 ≥ 5%：價強。",
            "- 週均量 ≥ 前 20 交易日日均量 1.5 倍：量強。",
            "- 細分 Theme 至少 3 檔價強，且上漲家數比 ≥ 60%：週訊號 PASS。",
            "- 同一股票可屬多個細分 Theme；各 Theme 內部對股票去重。",
            "- 機器人族群聚合口徑包含相關自動化 Theme，因此 28 檔不等同於 26 檔核准核心池。",
            "",
        ]
    )

    md_path = (
        args.output_file.resolve()
        if args.output_file
        else output_dir / f"robotics_subtheme_weekly_report_{latest_date}.md"
    )
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {md_path}")
    print(f"PASS themes: {len(passed)}")
    print(f"Formal robotics pool stocks: {formal_pool_stock_count}")
    print(f"New detailed stocks: {new_detailed_stock_count}")
    print(f"Detailed mappings: {detailed_mapping_count}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


APPROVED = {"approved", "auto_approved"}

AI_TAXONOMY = [
    {
        "layer": "運算系統",
        "theme": "AI_SERVER",
        "name": "AI伺服器",
        "action": "保留",
        "scope": "AI伺服器、加速運算伺服器與整機／系統級ODM",
        "exclude": "僅供應單一零組件者",
    },
    {
        "layer": "資料中心平台",
        "theme": "DATA_CENTER",
        "name": "資料中心",
        "action": "澄清邊界",
        "scope": "資料中心基礎設施平台、整體電力或機房級解決方案",
        "exclude": "單一伺服器或一般雲端軟體",
    },
    {
        "layer": "熱管理",
        "theme": "COOLING",
        "name": "散熱",
        "action": "保留為父Theme",
        "scope": "AI伺服器風冷、液冷與熱管理總類",
        "exclude": "非資料中心用途的一般消費電子散熱",
    },
    {
        "layer": "熱管理",
        "theme": "LIQUID_COOLING",
        "name": "液冷",
        "action": "保留",
        "scope": "冷板、CDU、歧管、泵浦與液冷系統",
        "exclude": "只有一般風扇或熱管產品",
    },
    {
        "layer": "熱管理",
        "theme": "AI_COLD_PLATE_CDU",
        "name": "AI冷板／CDU",
        "action": "新增候選",
        "scope": "具體供應AI資料中心冷板、CDU或液冷關鍵模組",
        "exclude": "只有液冷概念但未揭露產品位置",
    },
    {
        "layer": "電源轉換",
        "theme": "POWER_SUPPLY / HVDC_AI_POWER",
        "name": "電源供應／HVDC 800V",
        "action": "澄清父子邊界",
        "scope": "POWER_SUPPLY涵蓋一般伺服器電源；HVDC只收AI資料中心高壓直流架構",
        "exclude": "兩個Theme使用完全相同證據而無AI專用佐證",
    },
    {
        "layer": "備援電力",
        "theme": "UPS_BBU / AI_SERVER_BBU",
        "name": "UPS／AI伺服器BBU",
        "action": "澄清父子邊界",
        "scope": "UPS_BBU為一般備援電力；AI_SERVER_BBU須有AI伺服器機櫃應用證據",
        "exclude": "僅有一般電池模組或消費電子電池",
    },
    {
        "layer": "機櫃供配電",
        "theme": "AI_POWER_RACK / AI_RACK_POWER_DISTRIBUTION",
        "name": "Power Rack／Busbar／PDB",
        "action": "保留並澄清",
        "scope": "Power Rack為系統級機櫃；配電Theme限Busbar、PDB等機櫃內配電",
        "exclude": "一般機構件或無配電功能的機櫃",
    },
    {
        "layer": "高速互連",
        "theme": "AI_SERVER_CONNECTOR / HIGH_POWER_CONNECTOR",
        "name": "AI伺服器連接器／大電流連接器",
        "action": "澄清功能邊界",
        "scope": "分開高速訊號互連與高功率大電流連接，不以同一證據重複核准",
        "exclude": "一般消費性連接器",
    },
    {
        "layer": "高速互連",
        "theme": "AI_HIGH_SPEED_CABLE",
        "name": "AI高速線纜／AEC",
        "action": "新增候選",
        "scope": "AI叢集高速銅纜、AEC或機櫃間高速線纜",
        "exclude": "一般電源線或低速消費性線材",
    },
    {
        "layer": "光網路",
        "theme": "CPO / OPTICAL_COMMUNICATION",
        "name": "CPO／光通訊",
        "action": "跨族群沿用",
        "scope": "沿用既有高速光通訊族群，作為AI基礎建設related關係",
        "exclude": "複製建立內容相同的新Theme",
    },
    {
        "layer": "機構系統",
        "theme": "AI_SERVER_CHASSIS",
        "name": "AI伺服器機殼",
        "action": "新增候選",
        "scope": "AI伺服器專用機殼、機箱與其機構設計",
        "exclude": "整櫃運算平台、Power Rack電源系統或一般金屬加工",
    },
    {
        "layer": "機構系統",
        "theme": "AI_RACK_SYSTEM",
        "name": "AI整櫃系統",
        "action": "新增候選",
        "scope": "具AI運算節點、網路與整櫃整合能力的rack-scale平台",
        "exclude": "單一機殼、一般伺服器或只提供機櫃供配電者",
    },
    {
        "layer": "儲存系統",
        "theme": "AI_STORAGE_SYSTEM",
        "name": "AI儲存系統",
        "action": "新增候選",
        "scope": "獨立儲存伺服器或平台，並明確連結AI、GPU Direct Storage或AI檢索工作負載",
        "exclude": "一般消費性SSD、一般儲存伺服器或僅為AI伺服器內建NVMe功能者",
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit the Theme portfolio and AI infrastructure taxonomy.")
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--output-file", type=Path, required=True)
    parser.add_argument("--run-number", default="")
    parser.add_argument("--head-sha", default="")
    return parser.parse_args()


def load(path: Path, required: bool = True) -> pd.DataFrame:
    if not path.exists():
        if required:
            raise FileNotFoundError(path)
        return pd.DataFrame()
    return pd.read_csv(path, dtype=str).fillna("")


def approved_rows(frame: pd.DataFrame, origin: str) -> pd.DataFrame:
    if frame.empty:
        return frame
    result = frame.loc[
        frame["status"].eq("active") & frame["approval_status"].isin(APPROVED)
    ].copy()
    result["mapping_origin"] = origin
    return result


def fmt_pct(value: object) -> str:
    if value == "" or pd.isna(value):
        return "—"
    return f"{float(value):.1f}%"


def main() -> None:
    args = parse_args()
    data_dir = args.data_dir.resolve()
    themes = load(data_dir / "theme_master.csv")
    groups = load(data_dir / "theme_group_master.csv")
    group_map = load(data_dir / "theme_group_map.csv")
    curated = approved_rows(load(data_dir / "stock_theme_map.csv"), "curated")
    auto = approved_rows(load(data_dir / "stock_theme_auto_map.csv", required=False), "official_auto")
    summary = load(data_dir / "theme_signal_summary.csv", required=False)
    weekly = load(data_dir / "weekly_signal.csv", required=False)
    weekly_summary = load(data_dir / "weekly_summary.csv", required=False)

    mapping = pd.concat([curated, auto], ignore_index=True)
    if mapping.empty:
        raise ValueError("No approved Theme mappings found")
    mapping["origin_rank"] = mapping["mapping_origin"].map({"curated": 0, "official_auto": 1})
    mapping = (
        mapping.sort_values("origin_rank")
        .drop_duplicates(["stock_id", "theme_id"], keep="first")
        .drop(columns="origin_rank")
    )

    active_themes = themes.loc[themes["status"].eq("active")].copy()
    active_groups = groups.loc[groups["status"].eq("active")].copy()
    active_group_map = group_map.loc[group_map["status"].eq("active")].copy()
    as_of = str(weekly_summary.iloc[0]["latest_date"]) if not weekly_summary.empty else "unknown"

    mapped_count = mapping.groupby("theme_id")["stock_id"].nunique().to_dict()
    curated_count = curated.groupby("theme_id")["stock_id"].nunique().to_dict()
    auto_count = auto.groupby("theme_id")["stock_id"].nunique().to_dict()
    parent_ids = set(active_themes.loc[active_themes["parent_theme_id"].ne(""), "parent_theme_id"])
    zero_ids = [theme_id for theme_id in active_themes["theme_id"] if mapped_count.get(theme_id, 0) == 0]
    zero_parents = [theme_id for theme_id in zero_ids if theme_id in parent_ids]
    zero_leaves = [theme_id for theme_id in zero_ids if theme_id not in parent_ids]

    group_rows = []
    for _, group in active_groups.iterrows():
        group_id = group["group_id"]
        theme_ids = active_group_map.loc[active_group_map["group_id"].eq(group_id), "theme_id"]
        group_mapping = mapping.loc[mapping["theme_id"].isin(theme_ids)]
        group_curated = curated.loc[curated["theme_id"].isin(theme_ids)]
        group_auto = auto.loc[auto["theme_id"].isin(theme_ids)]
        if not group_auto.empty and group_curated.empty:
            maturity = "官方廣覆蓋"
        elif not group_auto.empty:
            maturity = "混合"
        elif not group_curated.empty:
            maturity = "人工證據池"
        else:
            maturity = "尚未覆蓋"
        group_rows.append(
            {
                "group_id": group_id,
                "group_name": group["group_name"],
                "theme_count": len(theme_ids),
                "mapped_stocks": group_mapping["stock_id"].nunique(),
                "curated_stocks": group_curated["stock_id"].nunique(),
                "auto_stocks": group_auto["stock_id"].nunique(),
                "maturity": maturity,
            }
        )
    group_rows = sorted(group_rows, key=lambda row: (-row["mapped_stocks"], row["group_id"]))

    ai_theme_ids = active_group_map.loc[
        active_group_map["group_id"].eq("AI_INFRA"), "theme_id"
    ].tolist()
    theme_name = active_themes.set_index("theme_id")["theme_name"].to_dict()
    theme_parent = active_themes.set_index("theme_id")["parent_theme_id"].to_dict()
    summary_index = summary.set_index("theme_id") if not summary.empty else pd.DataFrame()
    ai_rows = []
    stock_sets: dict[str, set[str]] = {}
    anomalous_stock_ids: set[str] = set()
    excluded_anomalous_stock_ids: set[str] = set()
    if not weekly.empty:
        raw_return_col = (
            "weekly_return_raw_pct"
            if "weekly_return_raw_pct" in weekly.columns
            else "weekly_return_pct"
        )
        weekly_return = pd.to_numeric(weekly[raw_return_col], errors="coerce")
        anomaly_mask = weekly_return.lt(-45) | weekly_return.gt(65)
        if "corporate_action_suspect" in weekly.columns:
            anomaly_mask |= weekly["corporate_action_suspect"].astype(str).str.lower().eq("true")
        anomalous_stock_ids = set(weekly.loc[anomaly_mask, "stock_id"])
        if "signal_eligible" in weekly.columns:
            eligible = weekly["signal_eligible"].astype(str).str.lower().eq("true")
            excluded_anomalous_stock_ids = set(
                weekly.loc[anomaly_mask & ~eligible, "stock_id"]
            )
    unresolved_anomalous_stock_ids = anomalous_stock_ids - excluded_anomalous_stock_ids
    for theme_id in ai_theme_ids:
        stock_set = set(mapping.loc[mapping["theme_id"].eq(theme_id), "stock_id"])
        stock_sets[theme_id] = stock_set
        avg_return = ""
        up_ratio = ""
        if not summary.empty and theme_id in summary_index.index:
            row = summary_index.loc[theme_id]
            avg_return = row["avg_weekly_return_pct"]
            up_ratio = float(row["up_ratio"]) * 100 if row["up_ratio"] != "" else ""
        ai_rows.append(
            {
                "theme_id": theme_id,
                "theme_name": theme_name.get(theme_id, ""),
                "parent": theme_parent.get(theme_id, ""),
                "stocks": len(stock_set),
                "curated": curated_count.get(theme_id, 0),
                "avg_return": avg_return,
                "up_ratio": up_ratio,
                "return_warning": bool(stock_set & unresolved_anomalous_stock_ids),
            }
        )

    overlaps = []
    for index, left in enumerate(ai_theme_ids):
        for right in ai_theme_ids[index + 1 :]:
            left_set = stock_sets[left]
            right_set = stock_sets[right]
            if len(left_set) < 2 or len(right_set) < 2:
                continue
            intersection = left_set & right_set
            union = left_set | right_set
            if union and len(intersection) / len(union) >= 0.75:
                relation = "相同股票池" if left_set == right_set else "高度重疊"
                overlaps.append((left, right, relation, len(intersection), len(union)))

    run_label = f"GitHub Actions #{args.run_number}" if args.run_number else "GitHub Actions artifact"
    if args.head_sha:
        run_label += f"（{args.head_sha[:7]}）"

    price_warning_lines = []
    if excluded_anomalous_stock_ids:
        price_warning_lines.append(
            "- 已隔離疑似公司行動或價格不連續股票："
            + "、".join(sorted(excluded_anomalous_stock_ids))
            + "；正式 Theme 平均報酬與上漲比不納入這些觀測值。"
        )
    if unresolved_anomalous_stock_ids:
        price_warning_lines.append(
            "- 尚未隔離的極端週報酬股票："
            + "、".join(sorted(unresolved_anomalous_stock_ids))
            + "。相關 Theme 已標示不可判讀，須先核對除權、分割或其他公司行動。"
        )
    if not price_warning_lines:
        price_warning_lines = [
            "- 本期未偵測到需隔離或尚待核對的極端價格變動。"
        ]

    lines = [
        f"# Theme 產業架構盤點與 AI 基礎建設細分候選（{as_of}）",
        "",
        f"- 資料來源：{run_label}",
        f"- 市場資料基準日：{as_of}",
        f"- Active Theme：{len(active_themes)}；Active Theme Group：{len(active_groups)}",
        (
            f"- 核准映射：{len(mapping)} 筆、{mapping['stock_id'].nunique()} 檔股票；"
            f"人工證據 {len(curated)} 筆、官方自動分類 {len(auto)} 筆"
        ),
        "",
        "## 結論",
        "",
        "機器人已完成細分 Theme、證據矩陣、人工核准與週訊號，是目前最完整的人工題材樣板。其他產業已具備骨架，但成熟度不一致：半導體、生技、能源與航運主要依官方大分類；AI、PCB、被動元件與連接器則是小型人工證據池，仍需擴充與澄清邊界。",
        "",
        f"共有 {len(zero_ids)} 個 active Theme 尚無正式映射，其中 {len(zero_parents)} 個是結構父節點、{len(zero_leaves)} 個是真正尚未覆蓋的葉節點。父節點為零不一定是錯誤，但葉節點為零代表 taxonomy 已建立、證據池尚未完成。",
        "",
        "## Theme Group 覆蓋盤點",
        "",
        "| Theme Group | Theme數 | 正式股票數 | 人工池 | 官方自動 | 成熟度 |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for row in group_rows:
        lines.append(
            f"| {row['group_name']}（{row['group_id']}） | {row['theme_count']} | "
            f"{row['mapped_stocks']} | {row['curated_stocks']} | {row['auto_stocks']} | {row['maturity']} |"
        )

    lines.extend(
        [
            "",
            "## AI 基礎建設現況",
            "",
            "| Theme | 父Theme | 股票數 | 人工核准 | 平均週報酬 | 上漲比 |",
            "|---|---|---:|---:|---:|---:|",
        ]
    )
    for row in ai_rows:
        avg_return_text = fmt_pct(row["avg_return"])
        up_ratio_text = fmt_pct(row["up_ratio"])
        if row["return_warning"]:
            avg_return_text = f"⚠ 原始 {avg_return_text}"
            up_ratio_text = "⚠ 不可判讀"
        lines.append(
            f"| {row['theme_name']}（{row['theme_id']}） | {row['parent'] or '—'} | "
            f"{row['stocks']} | {row['curated']} | {avg_return_text} | {up_ratio_text} |"
        )

    lines.extend(["", "### 需要澄清的重疊", ""])
    if overlaps:
        for left, right, relation, intersection, union in overlaps:
            lines.append(
                f"- `{left}` 與 `{right}`：{relation}，交集 {intersection}／聯集 {union} 檔。"
            )
    else:
        lines.append("- 未發現 75% 以上的股票池重疊。")

    lines.extend(
        [
            "",
            "### 價格資料警示",
            "",
            *price_warning_lines,
            "",
            "## AI 基礎建設細分候選架構",
            "",
            "| 產業層 | Theme／候選Theme | 名稱 | 建議 | 納入範圍 | 排除範圍 |",
            "|---|---|---|---|---|---|",
        ]
    )
    for row in AI_TAXONOMY:
        lines.append(
            f"| {row['layer']} | `{row['theme']}` | {row['name']} | {row['action']} | "
            f"{row['scope']} | {row['exclude']} |"
        )

    lines.extend(
        [
            "",
            "## 建議執行順序",
            "",
            "1. 先修正或隔離除權／分割等公司行動造成的週報酬異常。",
            "2. 對現有 AI 基礎建設 Theme 做邊界去重，不先新增股票。",
            "3. 為 `AI_COLD_PLATE_CDU`、`AI_HIGH_SPEED_CABLE`、`AI_SERVER_CHASSIS`、`AI_RACK_SYSTEM`、`AI_STORAGE_SYSTEM` 建立證據候選池。",
            "4. CPO／光通訊沿用既有 Theme，新增 AI_INFRA 的 related 關係，避免重複 taxonomy。",
            "5. 完成公司證據矩陣後再交由使用者人工核准；價格 PASS 不作為概念股資格證據。",
            "",
        ]
    )

    output = args.output_file.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {output}")
    print(f"Active themes: {len(active_themes)}")
    print(f"Active groups: {len(active_groups)}")
    print(f"Approved mappings: {len(mapping)}")
    print(f"Zero-mapped parents: {len(zero_parents)}")
    print(f"Zero-mapped leaves: {len(zero_leaves)}")
    print(f"AI overlap warnings: {len(overlaps)}")


if __name__ == "__main__":
    main()

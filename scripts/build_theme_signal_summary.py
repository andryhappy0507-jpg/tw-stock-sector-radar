from __future__ import annotations

from pathlib import Path
import pandas as pd

DATA = Path("data")
WEEKLY = DATA / "weekly_signal.csv"
THEME_MASTER = DATA / "theme_master.csv"
CURATED_THEME_MAP = DATA / "stock_theme_map.csv"
AUTO_THEME_MAP = DATA / "stock_theme_auto_map.csv"
GROUP_MASTER = DATA / "theme_group_master.csv"
GROUP_MAP = DATA / "theme_group_map.csv"
THEME_OUT = DATA / "theme_signal_summary.csv"
GROUP_OUT = DATA / "theme_group_signal_summary.csv"


def aggregate(df: pd.DataFrame, key: str, name_col: str) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=[
            key, name_col, "mapped_stock_count", "avg_weekly_return_pct",
            "up_ratio", "price_strong_count", "volume_strong_count",
            "A_count", "B_count", "C_count"
        ])

    # A stock can have multiple child themes in the same group; count it once per aggregation key.
    df = df.drop_duplicates([key, "stock_id"]).copy()
    rows = []
    for value, g in df.groupby(key, dropna=False):
        name = g[name_col].dropna().astype(str).iloc[0] if name_col in g and len(g[name_col].dropna()) else ""
        valid_ret = pd.to_numeric(g["weekly_return_pct"], errors="coerce")
        eligible_ret = valid_ret.loc[valid_ret.notna()]
        rows.append({
            key: value,
            name_col: name,
            "mapped_stock_count": int(g["stock_id"].nunique()),
            "avg_weekly_return_pct": float(eligible_ret.mean()) if not eligible_ret.empty else None,
            "up_ratio": float((eligible_ret > 0).mean()) if not eligible_ret.empty else None,
            "price_strong_count": int(g["price_strong"].fillna(False).astype(bool).sum()),
            "volume_strong_count": int(g["volume_strong"].fillna(False).astype(bool).sum()),
            "A_count": int((g["abc_group"] == "A").sum()),
            "B_count": int((g["abc_group"] == "B").sum()),
            "C_count": int((g["abc_group"] == "C").sum()),
        })
    return pd.DataFrame(rows).sort_values(
        ["A_count", "C_count", "avg_weekly_return_pct"],
        ascending=[False, False, False], na_position="last"
    )


def load_mapping() -> pd.DataFrame:
    frames = []
    for path in (CURATED_THEME_MAP, AUTO_THEME_MAP):
        if path.exists():
            df = pd.read_csv(path, dtype=str).fillna("")
            df["mapping_origin"] = "curated" if path == CURATED_THEME_MAP else "official_auto"
            frames.append(df)
    if not frames:
        raise FileNotFoundError("缺少 Theme mapping")
    mapping = pd.concat(frames, ignore_index=True)
    # Curated evidence wins if the same stock+theme also exists in the broad official layer.
    mapping["origin_rank"] = mapping["mapping_origin"].map({"curated": 0, "official_auto": 1}).fillna(9)
    mapping = mapping.sort_values("origin_rank").drop_duplicates(["stock_id", "theme_id"], keep="first")
    return mapping.drop(columns=["origin_rank"])


def main():
    for path in (WEEKLY, THEME_MASTER, GROUP_MASTER, GROUP_MAP):
        if not path.exists():
            raise FileNotFoundError(f"缺少必要檔案：{path}")

    weekly = pd.read_csv(WEEKLY, dtype={"stock_id": str})
    themes = pd.read_csv(THEME_MASTER, dtype=str).fillna("")
    mapping = load_mapping()
    group_master = pd.read_csv(GROUP_MASTER, dtype=str).fillna("")
    group_map = pd.read_csv(GROUP_MAP, dtype=str).fillna("")

    active_mapping = mapping.loc[
        mapping["status"].eq("active") & mapping["approval_status"].isin(["auto_approved", "approved"])
    ].copy()

    theme_join = active_mapping.merge(
        themes[["theme_id", "theme_name"]], on="theme_id", how="left"
    ).merge(weekly, on="stock_id", how="left")
    theme_summary = aggregate(theme_join, "theme_id", "theme_name")
    theme_summary.to_csv(THEME_OUT, index=False, encoding="utf-8-sig")

    group_join = active_mapping.merge(group_map.loc[group_map["status"].eq("active")], on="theme_id", how="inner")
    group_join = group_join.merge(group_master[["group_id", "group_name"]], on="group_id", how="left")
    group_join = group_join.merge(weekly, on="stock_id", how="left")
    group_summary = aggregate(group_join, "group_id", "group_name")
    group_summary.to_csv(GROUP_OUT, index=False, encoding="utf-8-sig")

    print(f"Active Theme mappings (curated+official auto): {len(active_mapping)}")
    print(f"Fine-theme summary: {len(theme_summary)} 個 Theme")
    print(f"Related-group summary: {len(group_summary)} 個族群")
    print("族群統計已對同一股票去重，避免一檔同時屬於多個子Theme時重複計算。")


if __name__ == "__main__":
    main()

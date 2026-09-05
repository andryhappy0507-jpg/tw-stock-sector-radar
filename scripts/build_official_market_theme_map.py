from __future__ import annotations

from pathlib import Path
import pandas as pd

DATA = Path("data")
CLASSIFICATION = DATA / "stock_classification_master.csv"
RULES = DATA / "official_market_theme_rules.csv"
THEME_MASTER = DATA / "theme_master.csv"
OUT = DATA / "stock_theme_auto_map.csv"


def normalize_code(value) -> str:
    text = "" if pd.isna(value) else str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    return text.zfill(2) if text.isdigit() else text


def main():
    stocks = pd.read_csv(CLASSIFICATION, dtype={"stock_id": str})
    rules = pd.read_csv(RULES, dtype=str).fillna("")
    themes = pd.read_csv(THEME_MASTER, dtype=str).fillna("")

    rules["industry_code"] = rules["industry_code"].map(normalize_code)
    stocks["industry_code"] = stocks["official_industry_code"].map(normalize_code)

    valid_theme_ids = set(themes.loc[themes["status"].eq("active"), "theme_id"])
    bad = rules.loc[~rules["theme_id"].isin(valid_theme_ids)]
    if not bad.empty:
        raise SystemExit(f"official market theme rules 含不存在 Theme: {bad.to_dict('records')}")

    eligible = stocks.loc[stocks["security_type"].eq("company_stock")].copy()
    out = eligible[["stock_id", "stock_name", "market", "industry_code"]].merge(
        rules, on="industry_code", how="inner"
    )
    out["source_type"] = "official_industry"
    out["source_date"] = ""
    out["source_ref"] = "TWSE/TPEx official industry classification"
    out["evidence_summary"] = out["reason"]
    out["last_verified"] = pd.Timestamp.now(tz="Asia/Taipei").date().isoformat()
    out["status"] = "active"
    out["approval_status"] = "auto_approved"
    out = out[[
        "stock_id", "theme_id", "confidence", "source_type", "source_date",
        "source_ref", "evidence_summary", "last_verified", "status", "approval_status"
    ]].drop_duplicates(["stock_id", "theme_id"])
    out.to_csv(OUT, index=False, encoding="utf-8-sig")

    print(f"Official-industry market Theme mappings: {len(out)} 筆")
    print(f"Covered company_stock: {out['stock_id'].nunique()} 檔")
    print("Theme counts:")
    print(out["theme_id"].value_counts().to_string())


if __name__ == "__main__":
    main()

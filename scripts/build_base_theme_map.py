from __future__ import annotations

from pathlib import Path
import pandas as pd

DATA = Path("data")
CLASSIFICATION = DATA / "stock_classification_master.csv"
BASE_MASTER = DATA / "base_theme_master.csv"
OUT = DATA / "stock_base_theme_map.csv"


def normalize_code(value) -> str:
    text = "" if pd.isna(value) else str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    return text.zfill(2) if text.isdigit() else text


def main():
    stocks = pd.read_csv(CLASSIFICATION, dtype={"stock_id": str})
    themes = pd.read_csv(BASE_MASTER, dtype=str).fillna("")
    themes["industry_code"] = themes["industry_code"].map(normalize_code)

    eligible = stocks.loc[stocks["security_type"].eq("company_stock")].copy()
    eligible["industry_code"] = eligible["official_industry_code"].map(normalize_code)

    out = eligible[["stock_id", "stock_name", "market", "industry_code"]].merge(
        themes[["theme_id", "theme_name", "industry_code", "source_ref"]],
        on="industry_code", how="left"
    )

    missing = out["theme_id"].isna() | out["theme_id"].eq("")
    if missing.any():
        rows = out.loc[missing, ["stock_id", "stock_name", "industry_code"]].to_dict("records")
        raise SystemExit(f"Base Theme 缺少產業代碼對照：{rows[:20]}")

    out["confidence"] = "high"
    out["source_type"] = "official_industry"
    out["evidence_summary"] = "依TWSE/TPEx官方產業代碼建立全市場基礎Theme"
    out["status"] = "active"
    out["approval_status"] = "auto_approved"
    out.to_csv(OUT, index=False, encoding="utf-8-sig")

    print(f"Base Theme mapping: {len(out)} 筆 / eligible company_stock {len(eligible)} 檔")
    print(f"Base Theme coverage: {out['stock_id'].nunique()}/{eligible['stock_id'].nunique()} = 100.00%")


if __name__ == "__main__":
    main()

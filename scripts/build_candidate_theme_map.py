from __future__ import annotations

from pathlib import Path
import pandas as pd

DATA = Path("data")
CLASSIFICATION = DATA / "stock_classification_master.csv"
THEME_MASTER = DATA / "theme_master.csv"
SOURCES = DATA / "theme_candidate_sources.csv"
OUT = DATA / "stock_theme_candidate_map.csv"


def main():
    stocks = pd.read_csv(CLASSIFICATION, dtype={"stock_id": str}).fillna("")
    themes = pd.read_csv(THEME_MASTER, dtype=str).fillna("")
    sources = pd.read_csv(SOURCES, dtype=str).fillna("")

    eligible = set(stocks.loc[stocks["security_type"].eq("company_stock"), "stock_id"])
    valid_themes = set(themes.loc[themes["status"].eq("active"), "theme_id"])

    rows = []
    skipped = []
    for _, src in sources.iterrows():
        theme_id = src["theme_id"].strip()
        if theme_id not in valid_themes:
            raise SystemExit(f"候選 Theme 不存在或非 active：{theme_id}")

        ids = [x.strip() for x in src["stock_ids"].split(";") if x.strip()]
        for stock_id in ids:
            if stock_id not in eligible:
                skipped.append((stock_id, theme_id))
                continue
            rows.append({
                "stock_id": stock_id,
                "theme_id": theme_id,
                "confidence": "medium",
                "source_type": "tpex_industry_value_chain",
                "source_date": "2026-08-23",
                "source_ref": src["source_ref"],
                "evidence_summary": src["evidence_summary"],
                "last_verified": "2026-08-23",
                "status": "watch",
                "approval_status": "pending",
            })

    out = pd.DataFrame(rows).drop_duplicates(["stock_id", "theme_id"]).sort_values(["theme_id", "stock_id"])
    out.to_csv(OUT, index=False, encoding="utf-8-sig")

    print(f"Candidate Theme mappings: {len(out)} 筆")
    print(f"Candidate covered company_stock: {out['stock_id'].nunique()} 檔")
    print("Candidate theme counts:")
    print(out["theme_id"].value_counts().to_string())
    if skipped:
        print(f"Skipped non-current/non-company mappings: {len(skipped)} -> {skipped[:20]}")


if __name__ == "__main__":
    main()

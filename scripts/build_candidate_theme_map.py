from __future__ import annotations

from pathlib import Path
import pandas as pd

DATA = Path("data")
CLASSIFICATION = DATA / "stock_classification_master.csv"
THEME_MASTER = DATA / "theme_master.csv"
SOURCES = DATA / "theme_candidate_sources.csv"
INDUSTRY_RULES = DATA / "candidate_industry_rules.csv"
OUT = DATA / "stock_theme_candidate_map.csv"

# Legacy source aliases keep historical source files backward compatible while
# preventing a broad official industry chain from being labeled too narrowly.
SOURCE_THEME_ALIASES = {
    "LOW_ORBIT_SATELLITE": "SATELLITE",
}


def candidate_row(stock_id: str, theme_id: str, source_type: str, source_ref: str, evidence: str) -> dict:
    return {
        "stock_id": stock_id,
        "theme_id": theme_id,
        "confidence": "medium",
        "source_type": source_type,
        "source_date": "2026-08-23",
        "source_ref": source_ref,
        "evidence_summary": evidence,
        "last_verified": "2026-08-23",
        "status": "watch",
        "approval_status": "pending",
    }


def main():
    stocks = pd.read_csv(CLASSIFICATION, dtype={"stock_id": str, "official_industry_code": str}).fillna("")
    themes = pd.read_csv(THEME_MASTER, dtype=str).fillna("")
    sources = pd.read_csv(SOURCES, dtype=str).fillna("")

    eligible_stocks = stocks.loc[stocks["security_type"].eq("company_stock")].copy()
    eligible = set(eligible_stocks["stock_id"])
    valid_themes = set(themes.loc[themes["status"].eq("active"), "theme_id"])

    rows = []
    skipped = []
    for _, src in sources.iterrows():
        source_theme_id = src["theme_id"].strip()
        theme_id = SOURCE_THEME_ALIASES.get(source_theme_id, source_theme_id)
        if theme_id not in valid_themes:
            raise SystemExit(f"候選 Theme 不存在或非 active：{theme_id}")

        ids = [x.strip() for x in src["stock_ids"].split(";") if x.strip()]
        for stock_id in ids:
            if stock_id not in eligible:
                skipped.append((stock_id, theme_id))
                continue
            evidence = src["evidence_summary"].strip()
            if source_theme_id == "LOW_ORBIT_SATELLITE":
                evidence += "；此來源為廣義太空衛星科技產業鏈，不直接等同低軌衛星"
            rows.append(candidate_row(
                stock_id,
                theme_id,
                "tpex_industry_value_chain",
                src["source_ref"],
                evidence,
            ))

    if INDUSTRY_RULES.exists():
        rules = pd.read_csv(INDUSTRY_RULES, dtype=str).fillna("")
        normalized_codes = eligible_stocks["official_industry_code"].str.replace(".0", "", regex=False)
        for _, rule in rules.iterrows():
            theme_id = rule["theme_id"].strip()
            industry_code = rule["industry_code"].strip()
            if theme_id not in valid_themes:
                raise SystemExit(f"官方產業候選 Theme 不存在或非 active：{theme_id}")
            matched = eligible_stocks.loc[normalized_codes.eq(industry_code), "stock_id"]
            for stock_id in matched:
                rows.append(candidate_row(
                    stock_id,
                    theme_id,
                    "official_industry_classification",
                    rule["source_ref"].strip() or "official_openapi",
                    rule["evidence_summary"].strip(),
                ))

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

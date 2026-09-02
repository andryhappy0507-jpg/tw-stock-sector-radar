from __future__ import annotations

from pathlib import Path
import pandas as pd


DATA = Path("data")
REVIEW = DATA / "research" / "robotics_subtheme_evidence_review_2026-09-02.csv"
FORMAL = DATA / "stock_theme_map.csv"
APPROVAL_DATE = "2026-09-02"

DIRECT_HIGH_SOURCES = {
    "company_website",
    "annual_report",
    "investor_conference",
    "mops",
    "management_transcript",
    "company_announcement",
}

SOURCE_TYPE_MAP = {
    "company_official": "company_website",
    "parent_company_official": "company_website",
    "company_prospectus": "company_website",
}


def formal_confidence(research_confidence: str, source_type: str) -> str:
    if research_confidence == "high" and source_type in DIRECT_HIGH_SOURCES:
        return "high"
    return "medium"


def main() -> None:
    review = pd.read_csv(REVIEW, dtype=str).fillna("")
    formal = pd.read_csv(FORMAL, dtype=str).fillna("")

    mask = (
        review["market_eligibility"].eq("listed_otc")
        & review["user_review_status"].eq("awaiting_user_review")
    )
    approved = review.loc[mask].copy()
    if approved.empty:
        finalized = review.loc[
            review["market_eligibility"].eq("listed_otc")
            & review["user_review_status"].eq("reviewed")
            & review["user_decision"].eq("approved")
        ]
        finalized_keys = set(zip(finalized["stock_id"], finalized["theme_id"]))
        formal_keys = set(zip(formal["stock_id"], formal["theme_id"]))
        if len(finalized) == 52 and finalized_keys <= formal_keys:
            print("52 筆機器人細分 mapping 已完成正式核准，無需重複處理")
            return
        raise RuntimeError("找不到待核准資料，且既有正式化狀態不完整")
    if len(approved) != 52:
        raise RuntimeError(f"預期核准 52 筆上市櫃映射，實際為 {len(approved)} 筆")

    existing_keys = set(zip(formal["stock_id"], formal["theme_id"]))
    approved_keys = list(zip(approved["stock_id"], approved["theme_id"]))
    duplicate_keys = sorted(set(approved_keys) & existing_keys)
    if duplicate_keys:
        raise RuntimeError(f"正式 mapping 已存在，停止避免重複：{duplicate_keys}")

    rows = []
    for _, row in approved.iterrows():
        source_type = SOURCE_TYPE_MAP.get(row["source_type"], row["source_type"])
        rows.append({
            "stock_id": row["stock_id"],
            "theme_id": row["theme_id"],
            "confidence": formal_confidence(row["confidence"], source_type),
            "source_type": source_type,
            "source_date": row["published_date"],
            "source_ref": row["source_url"],
            "evidence_summary": row["evidence_summary"],
            "last_verified": APPROVAL_DATE,
            "status": "active",
            "approval_status": "approved",
        })

    formal = pd.concat([formal, pd.DataFrame(rows)], ignore_index=True)
    if formal.duplicated(["stock_id", "theme_id"]).any():
        raise RuntimeError("正式 mapping 產生重複 stock_id + theme_id")

    review.loc[mask, "user_review_status"] = "reviewed"
    review.loc[mask, "user_decision"] = "approved"
    review.loc[mask, "user_note"] = "2026-09-02 user approved 52 robotics subtheme mappings"

    formal.to_csv(FORMAL, index=False, encoding="utf-8-sig")
    review.to_csv(REVIEW, index=False, encoding="utf-8-sig")

    print(f"正式新增 {len(rows)} 筆機器人細分 mapping")
    print("東佑達 4 筆興櫃觀察 mapping 保留於 research staging")


if __name__ == "__main__":
    main()

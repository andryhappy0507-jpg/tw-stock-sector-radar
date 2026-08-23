from __future__ import annotations

from pathlib import Path
import pandas as pd

DATA = Path("data")
CLASSIFICATION = DATA / "stock_classification_master.csv"
THEME_MASTER = DATA / "theme_master.csv"
CANDIDATES = DATA / "stock_theme_candidate_map.csv"

REQUIRED_COLUMNS = {
    "stock_id",
    "theme_id",
    "confidence",
    "source_type",
    "source_date",
    "source_ref",
    "evidence_summary",
    "last_verified",
    "status",
    "approval_status",
}


def fail(message: str) -> None:
    raise SystemExit(f"Candidate Theme validation failed: {message}")


def main() -> None:
    stocks = pd.read_csv(CLASSIFICATION, dtype=str).fillna("")
    themes = pd.read_csv(THEME_MASTER, dtype=str).fillna("")
    candidates = pd.read_csv(CANDIDATES, dtype=str).fillna("")

    missing = REQUIRED_COLUMNS - set(candidates.columns)
    if missing:
        fail(f"缺少欄位 {sorted(missing)}")

    if candidates.empty:
        fail("候選 Theme mapping 為空")

    duplicate_mask = candidates.duplicated(["stock_id", "theme_id"], keep=False)
    if duplicate_mask.any():
        dupes = candidates.loc[duplicate_mask, ["stock_id", "theme_id"]].head(20).to_dict("records")
        fail(f"存在重複 stock_id/theme_id：{dupes}")

    eligible = set(stocks.loc[stocks["security_type"].eq("company_stock"), "stock_id"])
    invalid_stocks = sorted(set(candidates["stock_id"]) - eligible)
    if invalid_stocks:
        fail(f"含非現行 company_stock：{invalid_stocks[:20]}")

    active_themes = set(themes.loc[themes["status"].eq("active"), "theme_id"])
    invalid_themes = sorted(set(candidates["theme_id"]) - active_themes)
    if invalid_themes:
        fail(f"含不存在或非 active Theme：{invalid_themes[:20]}")

    allowed_confidence = {"medium", "low"}
    bad_confidence = candidates.loc[~candidates["confidence"].isin(allowed_confidence), ["stock_id", "theme_id", "confidence"]]
    if not bad_confidence.empty:
        fail(f"候選 confidence 必須為 medium/low：{bad_confidence.head(20).to_dict('records')}")

    bad_status = candidates.loc[candidates["status"].ne("watch"), ["stock_id", "theme_id", "status"]]
    if not bad_status.empty:
        fail(f"候選 status 必須維持 watch：{bad_status.head(20).to_dict('records')}")

    bad_approval = candidates.loc[candidates["approval_status"].ne("pending"), ["stock_id", "theme_id", "approval_status"]]
    if not bad_approval.empty:
        fail(f"候選 approval_status 必須維持 pending：{bad_approval.head(20).to_dict('records')}")

    required_text = ["source_type", "source_ref", "evidence_summary"]
    for col in required_text:
        blank = candidates.loc[candidates[col].str.strip().eq(""), ["stock_id", "theme_id", col]]
        if not blank.empty:
            fail(f"{col} 不可空白：{blank.head(20).to_dict('records')}")

    print(f"Candidate Theme mappings validated: {len(candidates)} 筆")
    print(f"Candidate covered company_stock: {candidates['stock_id'].nunique()} 檔")
    print(f"Candidate themes: {candidates['theme_id'].nunique()} 個")
    print("Candidate Theme validation passed")


if __name__ == "__main__":
    main()

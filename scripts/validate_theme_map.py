from __future__ import annotations

from pathlib import Path
import pandas as pd

DATA = Path("data")
CLASSIFICATION = DATA / "stock_classification_master.csv"
THEME_MASTER = DATA / "theme_master.csv"
THEME_MAP = DATA / "stock_theme_map.csv"

VALID_CONFIDENCE = {"high", "medium", "low"}
VALID_STATUS = {"active", "watch", "stale", "inactive"}
VALID_APPROVAL = {"auto_approved", "approved", "pending", "rejected"}
DIRECT_HIGH_SOURCES = {
    "company_announcement",
    "company_website",
    "mops",
    "investor_conference",
    "annual_report",
    "management_transcript",
}


def main():
    for path in (CLASSIFICATION, THEME_MASTER, THEME_MAP):
        if not path.exists():
            raise FileNotFoundError(f"缺少必要檔案：{path}")

    stocks = pd.read_csv(CLASSIFICATION, dtype={"stock_id": str})
    themes = pd.read_csv(THEME_MASTER, dtype=str).fillna("")
    mappings = pd.read_csv(THEME_MAP, dtype=str).fillna("")

    company_ids = set(
        stocks.loc[stocks["security_type"].eq("company_stock"), "stock_id"].astype(str)
    )
    valid_theme_ids = set(themes.loc[themes["status"].ne("inactive"), "theme_id"].astype(str))

    errors = []
    warnings = []

    for idx, row in mappings.iterrows():
        line = idx + 2
        stock_id = row.get("stock_id", "").strip()
        theme_id = row.get("theme_id", "").strip()
        confidence = row.get("confidence", "").strip().lower()
        source_type = row.get("source_type", "").strip().lower()
        status = row.get("status", "").strip().lower()
        approval = row.get("approval_status", "").strip().lower()
        evidence = row.get("evidence_summary", "").strip()
        source_ref = row.get("source_ref", "").strip()

        if stock_id not in company_ids:
            errors.append(f"L{line}: {stock_id} 不是已確認 company_stock")
        if theme_id not in valid_theme_ids:
            errors.append(f"L{line}: theme_id={theme_id} 不存在或已 inactive")
        if confidence not in VALID_CONFIDENCE:
            errors.append(f"L{line}: confidence={confidence} 非法")
        if status not in VALID_STATUS:
            errors.append(f"L{line}: status={status} 非法")
        if approval not in VALID_APPROVAL:
            errors.append(f"L{line}: approval_status={approval} 非法")
        if not evidence:
            errors.append(f"L{line}: 缺 evidence_summary")
        if not source_ref:
            errors.append(f"L{line}: 缺 source_ref")

        if confidence == "high" and source_type not in DIRECT_HIGH_SOURCES:
            warnings.append(
                f"L{line}: high 但 source_type={source_type} 不是直接官方/管理層證據，建議人工覆核"
            )
        if confidence in {"medium", "low"} and approval == "auto_approved":
            errors.append(f"L{line}: medium/low 不可 auto_approved，需人工核准")

    duplicate_mask = mappings.duplicated(["stock_id", "theme_id"], keep=False) if len(mappings) else []
    if len(mappings) and duplicate_mask.any():
        dup = mappings.loc[duplicate_mask, ["stock_id", "theme_id"]].drop_duplicates()
        for _, row in dup.iterrows():
            errors.append(f"重複 mapping: {row['stock_id']} + {row['theme_id']}")

    print(f"Theme master: {len(themes)} 個題材")
    print(f"Theme mappings: {len(mappings)} 筆")
    print(f"可掛 Theme 的 company_stock: {len(company_ids)} 檔")

    for warning in warnings:
        print("WARNING:", warning)

    if errors:
        for error in errors:
            print("ERROR:", error)
        raise SystemExit(f"Theme mapping 驗證失敗：{len(errors)} 個錯誤")

    print("Theme mapping 驗證通過")


if __name__ == "__main__":
    main()

from __future__ import annotations

from pathlib import Path
import pandas as pd

DATA = Path("data")
RULES = DATA / "theme_coverage_rules.csv"
FORMAL = DATA / "stock_theme_map.csv"
OUT = DATA / "theme_coverage_summary.csv"

VALID_COVERAGE_STATUS = {"discovery", "auditing", "coverage_ready"}


def split_ids(value: str) -> set[str]:
    return {x.strip() for x in str(value).split(";") if x.strip()}


def main() -> None:
    if not RULES.exists():
        raise SystemExit(f"missing coverage rules: {RULES}")
    if not FORMAL.exists():
        raise SystemExit(f"missing formal theme map: {FORMAL}")

    rules = pd.read_csv(RULES, dtype=str).fillna("")
    formal = pd.read_csv(FORMAL, dtype=str).fillna("")

    required_rule_cols = {
        "theme_id", "priority", "coverage_status", "require_manual_review",
        "coverage_audit_path", "discovery_keywords", "related_theme_ids",
    }
    missing = required_rule_cols - set(rules.columns)
    if missing:
        raise SystemExit(f"theme_coverage_rules.csv missing columns: {sorted(missing)}")

    rows: list[dict[str, object]] = []
    for _, rule in rules.iterrows():
        theme_id = rule["theme_id"].strip()
        coverage_status = rule["coverage_status"].strip()
        if not theme_id:
            raise SystemExit("empty theme_id in coverage rules")
        if coverage_status not in VALID_COVERAGE_STATUS:
            raise SystemExit(f"invalid coverage_status for {theme_id}: {coverage_status}")

        related = split_ids(rule["related_theme_ids"])
        universe_theme_ids = {theme_id} | related

        formal_mask = (
            formal["theme_id"].isin(universe_theme_ids)
            & formal["status"].eq("active")
            & formal["approval_status"].isin(["approved", "auto_approved"])
        )
        formal_ids = set(formal.loc[formal_mask, "stock_id"])

        audit_path = Path(rule["coverage_audit_path"].strip())
        if not audit_path.exists():
            raise SystemExit(f"coverage audit file missing for {theme_id}: {audit_path}")
        audit = pd.read_csv(audit_path, dtype=str).fillna("")

        required_audit_cols = {
            "stock_id", "coverage_layer", "current_state", "next_action"
        }
        missing_audit = required_audit_cols - set(audit.columns)
        if missing_audit:
            raise SystemExit(
                f"{audit_path} missing columns for {theme_id}: {sorted(missing_audit)}"
            )

        pool_ids = set(audit["stock_id"])
        staging_ids = set(audit.loc[audit["coverage_layer"].eq("staging"), "stock_id"])
        awaiting_ids = set(
            audit.loc[audit["current_state"].eq("awaiting_user_review"), "stock_id"]
        )
        need_evidence_ids = set(
            audit.loc[
                audit["next_action"].isin(["need_evidence", "find_second_source"]),
                "stock_id",
            ]
        )
        suspected_missing_ids = set(
            audit.loc[
                audit["coverage_layer"].eq("discovery")
                | audit["current_state"].eq("suspected_missing"),
                "stock_id",
            ]
        )

        # Guardrail: coverage_ready is a completeness claim. It cannot coexist
        # with unresolved discovery/missing candidates.
        if coverage_status == "coverage_ready" and suspected_missing_ids:
            raise SystemExit(
                f"{theme_id} cannot be coverage_ready with suspected missing stocks: "
                f"{sorted(suspected_missing_ids)}"
            )

        rows.append({
            "theme_id": theme_id,
            "priority": rule["priority"].strip(),
            "coverage_status": coverage_status,
            "formal_approved_count": len(formal_ids),
            "coverage_pool_count": len(pool_ids),
            "staging_count": len(staging_ids),
            "awaiting_user_review_count": len(awaiting_ids),
            "need_evidence_count": len(need_evidence_ids),
            "suspected_missing_count": len(suspected_missing_ids),
            "discovery_keyword_count": len(split_ids(rule["discovery_keywords"])),
            "related_theme_count": len(related),
            "coverage_audit_path": str(audit_path),
        })

    out = pd.DataFrame(rows).sort_values(["priority", "theme_id"])
    out.to_csv(OUT, index=False, encoding="utf-8-sig")

    print("Theme coverage summary:")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()

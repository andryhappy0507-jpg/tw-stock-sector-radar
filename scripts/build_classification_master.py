from __future__ import annotations

from pathlib import Path
import requests
import pandas as pd

DATA = Path("data")
STOCK_MASTER = DATA / "stock_master.csv"
OUT = DATA / "stock_classification_master.csv"

TWSE_URL = "https://openapi.twse.com.tw/v1/opendata/t187ap03_L"
TPEX_URL = "https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap03_O"
HEADERS = {"User-Agent": "Mozilla/5.0 tw-stock-sector-radar/1.0"}


def clean_text(value) -> str:
    if value is None:
        return ""
    text = str(value).replace("\u3000", " ").strip()
    return "" if text in {"", "－", "-", "--", "nan", "None"} else text


def first_value(row: dict, names: list[str]):
    for name in names:
        if name in row and row[name] not in (None, ""):
            return row[name]
    return None


def normalize_company_rows(payload, market: str) -> pd.DataFrame:
    rows = payload if isinstance(payload, list) else payload.get("data", []) if isinstance(payload, dict) else []
    out = []

    if market == "TWSE":
        id_keys = ["公司代號", "股票代號", "證券代號"]
        name_keys = ["公司簡稱", "公司名稱", "股票名稱"]
        industry_keys = ["產業別", "產業類別"]
    else:
        # TPEx mopsfin_t187ap03_O uses English field names.
        id_keys = ["SecuritiesCompanyCode", "公司代號", "股票代號", "證券代號"]
        name_keys = ["CompanyAbbreviation", "CompanyName", "公司簡稱", "公司名稱"]
        industry_keys = ["SecuritiesIndustryCode", "產業別", "產業類別"]

    for row in rows:
        if not isinstance(row, dict):
            continue
        stock_id = clean_text(first_value(row, id_keys))
        if len(stock_id) != 4 or not stock_id.isdigit():
            continue

        name = clean_text(first_value(row, name_keys))
        industry_code = clean_text(first_value(row, industry_keys))
        if industry_code.endswith(".0"):
            industry_code = industry_code[:-2]
        industry_code = industry_code.zfill(2) if industry_code.isdigit() else industry_code

        out.append({
            "stock_id": stock_id,
            "official_company_name": name,
            "official_industry_code": industry_code,
            "official_market": market,
            "is_official_company": True,
        })

    return pd.DataFrame(out)


def fetch_json(session: requests.Session, url: str):
    r = session.get(url, headers=HEADERS, timeout=45)
    r.raise_for_status()
    return r.json()


def classify_security(row) -> str:
    if bool(row.get("is_official_company", False)):
        return "company_stock"

    stock_id = str(row.get("stock_id", "")).strip()
    name = str(row.get("stock_name", "")).upper()

    if stock_id.startswith("020") or "ETN" in name:
        return "ETN"
    if stock_id.startswith("00") or "ETF" in name:
        return "ETF"
    return "unclassified"


def main():
    if not STOCK_MASTER.exists():
        raise FileNotFoundError("data/stock_master.csv 尚未產生")

    master = pd.read_csv(STOCK_MASTER, dtype={"stock_id": str})
    session = requests.Session()

    frames = []
    for market, url in [("TWSE", TWSE_URL), ("TPEx", TPEX_URL)]:
        try:
            df = normalize_company_rows(fetch_json(session, url), market)
            print(f"{market} 官方公司基本資料：{len(df)} 檔")
            frames.append(df)
        except Exception as exc:
            print(f"{market} 官方產業資料抓取失敗：{exc}")

    official = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(
        columns=[
            "stock_id", "official_company_name", "official_industry_code",
            "official_market", "is_official_company"
        ]
    )
    official = official.drop_duplicates("stock_id", keep="last")

    enriched = master.merge(official, on="stock_id", how="left")
    enriched["is_official_company"] = enriched["is_official_company"].fillna(False).astype(bool)
    enriched["security_type"] = enriched.apply(classify_security, axis=1)
    enriched["include_in_equity_universe"] = enriched["security_type"].eq("company_stock")
    enriched["industry_source"] = enriched["is_official_company"].map(
        {True: "official_openapi", False: "not_applicable_or_pending"}
    )

    enriched.to_csv(OUT, index=False, encoding="utf-8-sig")

    counts = enriched["security_type"].value_counts().to_dict()
    official_count = int(enriched["is_official_company"].sum())
    industry_count = int(
        enriched.loc[enriched["is_official_company"], "official_industry_code"]
        .fillna("").astype(str).str.strip().ne("").sum()
    )
    industry_rate = (industry_count / official_count * 100.0) if official_count else 0.0

    print(f"輸出 {OUT}: {len(enriched)} 檔")
    print("證券類型統計：" + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    print(f"官方公司股產業代碼覆蓋率：{industry_count}/{official_count} = {industry_rate:.2f}%")


if __name__ == "__main__":
    main()

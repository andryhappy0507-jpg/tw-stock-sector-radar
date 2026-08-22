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


def first_value(row: dict, names: list[str]):
    for name in names:
        if name in row and row[name] not in (None, ""):
            return row[name]
    for key, value in row.items():
        if any(name in str(key) for name in names) and value not in (None, ""):
            return value
    return None


def normalize_company_rows(payload, market: str) -> pd.DataFrame:
    rows = payload if isinstance(payload, list) else payload.get("data", []) if isinstance(payload, dict) else []
    out = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        stock_id = str(first_value(row, ["公司代號", "股票代號", "證券代號"]) or "").strip()
        if len(stock_id) != 4 or not stock_id.isdigit():
            continue
        name = str(first_value(row, ["公司簡稱", "公司名稱", "股票名稱"]) or "").strip()
        industry = str(first_value(row, ["產業別", "產業類別"]) or "").strip()
        out.append({
            "stock_id": stock_id,
            "official_company_name": name,
            "official_industry": industry,
            "official_market": market,
            "is_official_company": True,
        })
    return pd.DataFrame(out)


def fetch_json(session: requests.Session, url: str):
    r = session.get(url, headers=HEADERS, timeout=45)
    r.raise_for_status()
    return r.json()


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
        columns=["stock_id", "official_company_name", "official_industry", "official_market", "is_official_company"]
    )
    official = official.drop_duplicates("stock_id", keep="last")

    enriched = master.merge(official, on="stock_id", how="left")
    enriched["is_official_company"] = enriched["is_official_company"].fillna(False).astype(bool)
    enriched["security_type"] = enriched["is_official_company"].map({True: "company_stock", False: "non_company_or_unclassified"})
    enriched["include_in_equity_universe"] = enriched["is_official_company"]
    enriched["industry_source"] = enriched["is_official_company"].map({True: "official_openapi", False: "unclassified"})

    enriched.to_csv(OUT, index=False, encoding="utf-8-sig")
    print(
        f"輸出 {OUT}: {len(enriched)} 檔；官方公司股 {int(enriched['is_official_company'].sum())} 檔；"
        f"待排除/待分類 {int((~enriched['is_official_company']).sum())} 檔"
    )


if __name__ == "__main__":
    main()

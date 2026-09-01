from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path
import re
import time
import requests
import pandas as pd

DATA = Path("data")
DATA.mkdir(exist_ok=True)
HEADERS = {"User-Agent": "Mozilla/5.0 tw-stock-sector-radar/1.0"}
TPEX_PAGE = "https://www.tpex.org.tw/zh-tw/mainboard/trading/info/stock-pricing.html"
TPEX_HEADERS = {
    **HEADERS,
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
    "Referer": TPEX_PAGE,
}
TPEX_EDGE_RETRY_STATUSES = {403, 429, 520, 521, 522, 523, 524}

TWSE_HIST = "https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX"
TPEX_HIST = "https://www.tpex.org.tw/www/zh-tw/afterTrading/dailyQuotes"
BACKFILL_TRADING_DAYS = 60
MAX_LOOKBACK_CALENDAR_DAYS = 110
MIN_TWSE_ROWS = 900
MIN_TPEX_ROWS = 700
RETRIES = 3


def number(v):
    if v is None:
        return None
    s = re.sub(r"[,+%]", "", str(v)).strip()
    s = s.replace("X", "").replace("=", "").replace('"', "")
    if s in {"", "--", "---", "除權", "除息"}:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def clean_header(v):
    return re.sub(r"<[^>]+>", "", str(v)).strip().replace("\u3000", "")


def table_from_payload(payload, required_headers):
    tables = payload.get("tables", []) if isinstance(payload, dict) else []
    for table in tables:
        fields = [clean_header(x) for x in table.get("fields", [])]
        if all(any(req in f for f in fields) for req in required_headers):
            return fields, table.get("data", [])
    return None, None


def find_col(fields, *names):
    for name in names:
        for i, field in enumerate(fields):
            if name in field:
                return i
    return None


def parse_rows(fields, data, trade_date, market):
    code_i = find_col(fields, "證券代號", "代號")
    name_i = find_col(fields, "證券名稱", "名稱")
    open_i = find_col(fields, "開盤價", "開盤")
    high_i = find_col(fields, "最高價", "最高")
    low_i = find_col(fields, "最低價", "最低")
    close_i = find_col(fields, "收盤價", "收盤")
    vol_i = find_col(fields, "成交股數", "成交量")
    val_i = find_col(fields, "成交金額")
    needed = [code_i, name_i, close_i, vol_i]
    if any(i is None for i in needed):
        raise RuntimeError(f"{market} 表格缺少必要欄位: {fields}")

    rows = []
    for row in data:
        if not isinstance(row, list):
            continue
        stock_id = str(row[code_i]).strip().replace('="', '').replace('"', '')
        if not re.fullmatch(r"\d{4}", stock_id):
            continue
        rows.append({
            "date": trade_date.isoformat(),
            "stock_id": stock_id,
            "stock_name": str(row[name_i]).strip(),
            "market": market,
            "open": number(row[open_i]) if open_i is not None else None,
            "high": number(row[high_i]) if high_i is not None else None,
            "low": number(row[low_i]) if low_i is not None else None,
            "close": number(row[close_i]),
            "volume_shares": number(row[vol_i]),
            "turnover_ntd": number(row[val_i]) if val_i is not None else None,
        })
    return pd.DataFrame(rows)


def fetch_twse_for_day(session, trade_date):
    params = {"date": trade_date.strftime("%Y%m%d"), "type": "ALLBUT0999", "response": "json"}
    r = session.get(TWSE_HIST, params=params, headers=HEADERS, timeout=40)
    r.raise_for_status()
    payload = r.json()
    fields, data = table_from_payload(payload, ["證券代號", "成交股數", "收盤價"])
    if not fields:
        return pd.DataFrame()
    return parse_rows(fields, data, trade_date, "TWSE")


def prepare_tpex_session(session):
    """Establish the TPEx session cookie expected by its Cloudflare edge."""
    r = session.get(TPEX_PAGE, headers=HEADERS, timeout=40)
    r.raise_for_status()


def fetch_tpex_for_day(session, trade_date):
    params = {"date": trade_date.strftime("%Y/%m/%d"), "id": "", "response": "json"}
    r = session.get(TPEX_HIST, params=params, headers=TPEX_HEADERS, timeout=40)
    if r.status_code in TPEX_EDGE_RETRY_STATUSES:
        # TPEx may expire or challenge the session used by hosted CI runners.
        # Refresh the first-party cookie once before the outer daily retry loop.
        prepare_tpex_session(session)
        time.sleep(0.75)
        r = session.get(TPEX_HIST, params=params, headers=TPEX_HEADERS, timeout=40)
    r.raise_for_status()
    payload = r.json()
    fields, data = table_from_payload(payload, ["代號", "成交", "收盤"])
    if not fields:
        return pd.DataFrame()
    return parse_rows(fields, data, trade_date, "TPEx")


def fetch_complete_day(session, trade_date):
    last_error = None
    for attempt in range(1, RETRIES + 1):
        try:
            twse = fetch_twse_for_day(session, trade_date)
            tpex = fetch_tpex_for_day(session, trade_date)
            twse_n, tpex_n = len(twse), len(tpex)
            if twse_n >= MIN_TWSE_ROWS and tpex_n >= MIN_TPEX_ROWS:
                print(f"{trade_date}: TWSE {twse_n} + TPEx {tpex_n} = {twse_n + tpex_n} PASS")
                return pd.concat([twse, tpex], ignore_index=True), None
            last_error = f"資料不完整：TWSE {twse_n}、TPEx {tpex_n}"
        except Exception as exc:
            last_error = str(exc)
        if attempt < RETRIES:
            time.sleep(1.0 * attempt)
    print(f"{trade_date}: FAIL - {last_error}")
    return pd.DataFrame(), last_error


def is_complete_in_existing(df, trade_date):
    day = df[df["date"] == trade_date.isoformat()]
    if day.empty or "market" not in day.columns:
        return False
    counts = day.groupby("market")["stock_id"].nunique().to_dict()
    return counts.get("TWSE", 0) >= MIN_TWSE_ROWS and counts.get("TPEx", 0) >= MIN_TPEX_ROWS


def merge_without_duplicates(old, new):
    if old is None or old.empty:
        merged = new.copy()
    else:
        merged = pd.concat([old, new], ignore_index=True)
    return merged.drop_duplicates(["date", "stock_id"], keep="last")


def backfill(session):
    print(f"market_data.csv 不存在：開始建立最近 {BACKFILL_TRADING_DAYS} 個完整交易日基準資料")
    collected = []
    trading_dates = 0
    cursor = date.today()
    checked = 0
    while trading_dates < BACKFILL_TRADING_DAYS and checked < MAX_LOOKBACK_CALENDAR_DAYS:
        if cursor.weekday() < 5:
            day_df, _ = fetch_complete_day(session, cursor)
            if not day_df.empty:
                collected.append(day_df)
                trading_dates += 1
                print(f"進度：{trading_dates}/{BACKFILL_TRADING_DAYS}")
            time.sleep(0.35)
        cursor -= timedelta(days=1)
        checked += 1

    if trading_dates < BACKFILL_TRADING_DAYS:
        raise RuntimeError(f"完整歷史回補不足，只取得 {trading_dates}/{BACKFILL_TRADING_DAYS} 個完整交易日")
    return pd.concat(collected, ignore_index=True)


def main():
    out = DATA / "market_data.csv"
    session = requests.Session()
    try:
        prepare_tpex_session(session)
    except Exception as exc:
        # The dated endpoint still gets its normal retries. This warning keeps a
        # transient landing-page failure from aborting before the first query.
        print(f"TPEx session warm-up warning: {exc}")

    if out.exists():
        old = pd.read_csv(out, dtype={"stock_id": str})
        old["date"] = old["date"].astype(str)
        frames = [old]

        existing_dates = sorted(pd.to_datetime(old["date"].unique()).date)
        repair_dates = [d for d in existing_dates if not is_complete_in_existing(old, d)]
        if repair_dates:
            print("偵測到不完整日期，只回補這些日期：" + ", ".join(map(str, repair_dates)))
            for d in repair_dates:
                part, _ = fetch_complete_day(session, d)
                if not part.empty:
                    old = old[old["date"] != d.isoformat()]
                    old = merge_without_duplicates(old, part)
                time.sleep(0.25)

        latest_date = pd.to_datetime(old["date"]).max().date()
        cursor = latest_date + timedelta(days=1)
        while cursor <= date.today():
            if cursor.weekday() < 5:
                part, _ = fetch_complete_day(session, cursor)
                if not part.empty:
                    old = merge_without_duplicates(old, part)
            cursor += timedelta(days=1)
            time.sleep(0.25)
        all_data = old
    else:
        all_data = backfill(session)

    all_data = all_data.dropna(subset=["close", "volume_shares"])
    all_data = all_data.drop_duplicates(["date", "stock_id"], keep="last")
    all_data = all_data.sort_values(["date", "stock_id"])
    all_data.to_csv(out, index=False, encoding="utf-8-sig")

    latest = all_data.sort_values("date").groupby("stock_id", as_index=False).tail(1)
    master = latest[["stock_id", "stock_name", "market"]].drop_duplicates("stock_id")
    master.sort_values(["market", "stock_id"]).to_csv(DATA / "stock_master.csv", index=False, encoding="utf-8-sig")

    unique_dates = all_data["date"].nunique()
    print(f"完成：market_data 共 {len(all_data)} 列、{unique_dates} 個交易日、{master['stock_id'].nunique()} 檔代號")


if __name__ == "__main__":
    main()

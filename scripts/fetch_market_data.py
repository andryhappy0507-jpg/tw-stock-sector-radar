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

TWSE_HIST = "https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX"
TPEX_HIST = "https://www.tpex.org.tw/www/zh-tw/afterTrading/dailyQuotes"
BACKFILL_TRADING_DAYS = 60
MAX_LOOKBACK_CALENDAR_DAYS = 110


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
    params = {
        "date": trade_date.strftime("%Y%m%d"),
        "type": "ALLBUT0999",
        "response": "json",
    }
    r = session.get(TWSE_HIST, params=params, headers=HEADERS, timeout=40)
    r.raise_for_status()
    payload = r.json()
    fields, data = table_from_payload(payload, ["證券代號", "成交股數", "收盤價"])
    if not fields:
        return pd.DataFrame()
    return parse_rows(fields, data, trade_date, "TWSE")


def fetch_tpex_for_day(session, trade_date):
    params = {
        "date": trade_date.strftime("%Y/%m/%d"),
        "id": "",
        "response": "json",
    }
    r = session.get(TPEX_HIST, params=params, headers=HEADERS, timeout=40)
    r.raise_for_status()
    payload = r.json()
    fields, data = table_from_payload(payload, ["代號", "成交", "收盤"])
    if not fields:
        # 部分版本不是 tables 結構；保守回傳空資料並讓下一次日更補齊。
        return pd.DataFrame()
    return parse_rows(fields, data, trade_date, "TPEx")


def fetch_day(session, trade_date):
    frames = []
    errors = []
    for name, fn in [("TWSE", fetch_twse_for_day), ("TPEx", fetch_tpex_for_day)]:
        try:
            part = fn(session, trade_date)
            if not part.empty:
                frames.append(part)
        except Exception as exc:
            errors.append(f"{name}: {exc}")
    if frames:
        return pd.concat(frames, ignore_index=True), errors
    return pd.DataFrame(), errors


def backfill(session):
    print(f"market_data.csv 不存在：開始自動回補最近 {BACKFILL_TRADING_DAYS} 個交易日")
    collected = []
    trading_dates = 0
    cursor = date.today()
    checked = 0
    while trading_dates < BACKFILL_TRADING_DAYS and checked < MAX_LOOKBACK_CALENDAR_DAYS:
        if cursor.weekday() < 5:
            day_df, errors = fetch_day(session, cursor)
            if not day_df.empty:
                collected.append(day_df)
                trading_dates += 1
                print(f"{cursor}: {len(day_df)} 筆（第 {trading_dates}/{BACKFILL_TRADING_DAYS} 個交易日）")
            elif errors:
                print(f"{cursor}: 無資料；{' | '.join(errors)}")
            time.sleep(0.35)
        cursor -= timedelta(days=1)
        checked += 1

    if trading_dates < 25:
        raise RuntimeError(f"歷史回補不足，只取得 {trading_dates} 個交易日；至少需要 25 日")
    return pd.concat(collected, ignore_index=True)


def main():
    out = DATA / "market_data.csv"
    session = requests.Session()

    if out.exists():
        old = pd.read_csv(out, dtype={"stock_id": str})
        latest_date = pd.to_datetime(old["date"]).max().date()
        # 補抓 latest_date 到今天之間所有平日，可修補 GitHub Actions 偶發漏跑。
        days = []
        cursor = latest_date
        while cursor <= date.today():
            if cursor.weekday() < 5:
                days.append(cursor)
            cursor += timedelta(days=1)
        frames = [old]
        for d in days:
            part, errors = fetch_day(session, d)
            if not part.empty:
                frames.append(part)
                print(f"更新 {d}: {len(part)} 筆")
            elif errors:
                print(f"{d}: {' | '.join(errors)}")
            time.sleep(0.25)
        all_data = pd.concat(frames, ignore_index=True)
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

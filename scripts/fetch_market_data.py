from __future__ import annotations

from datetime import date
from pathlib import Path
import io
import re
import requests
import pandas as pd

DATA = Path("data")
DATA.mkdir(exist_ok=True)
HEADERS = {"User-Agent": "tw-stock-sector-radar/1.0"}

TWSE_DAILY = "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"
# TPEx 官方每日收盤行情頁面提供 CSV；URL 若官方改版，只需修改這一處。
TPEX_DAILY_CSV = "https://www.tpex.org.tw/www/zh-tw/afterTrading/dailyQuotes?date={date}&id=&response=csv"


def number(v):
    if v is None:
        return None
    s = re.sub(r"[,+%]", "", str(v)).strip()
    if s in {"", "--", "---", "除權", "除息"}:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def fetch_twse() -> pd.DataFrame:
    r = requests.get(TWSE_DAILY, headers=HEADERS, timeout=30)
    r.raise_for_status()
    raw = r.json()
    rows = []
    for x in raw:
        stock_id = str(x.get("Code", "")).strip()
        if not re.fullmatch(r"\d{4}", stock_id):
            continue
        rows.append({
            "date": date.today().isoformat(),
            "stock_id": stock_id,
            "stock_name": x.get("Name"),
            "market": "TWSE",
            "open": number(x.get("OpeningPrice")),
            "high": number(x.get("HighestPrice")),
            "low": number(x.get("LowestPrice")),
            "close": number(x.get("ClosingPrice")),
            "volume_shares": number(x.get("TradeVolume")),
            "turnover_ntd": number(x.get("TradeValue")),
        })
    return pd.DataFrame(rows)


def fetch_tpex() -> pd.DataFrame:
    roc = date.today().strftime("%Y/%m/%d")
    r = requests.get(TPEX_DAILY_CSV.format(date=roc), headers=HEADERS, timeout=30)
    r.raise_for_status()
    text = r.content.decode("utf-8-sig", errors="replace")
    # 官方 CSV 格式可能含標題/註記；尋找包含代號的表頭開始解析。
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines) if "代號" in line and "名稱" in line), None)
    if start is None:
        raise RuntimeError("無法辨識 TPEx 每日行情 CSV 表頭")
    df = pd.read_csv(io.StringIO("\n".join(lines[start:])))
    df.columns = [str(c).strip().replace("\ufeff", "") for c in df.columns]

    def col(*names):
        for n in names:
            for c in df.columns:
                if n in c:
                    return c
        return None

    code_c, name_c = col("代號"), col("名稱")
    open_c, high_c, low_c, close_c = col("開盤"), col("最高"), col("最低"), col("收盤")
    vol_c, val_c = col("成交股數", "成交量"), col("成交金額")
    rows = []
    for _, x in df.iterrows():
        stock_id = str(x.get(code_c, "")).strip().replace('="', '').replace('"', '')
        if not re.fullmatch(r"\d{4}", stock_id):
            continue
        rows.append({
            "date": date.today().isoformat(), "stock_id": stock_id,
            "stock_name": x.get(name_c), "market": "TPEx",
            "open": number(x.get(open_c)), "high": number(x.get(high_c)),
            "low": number(x.get(low_c)), "close": number(x.get(close_c)),
            "volume_shares": number(x.get(vol_c)), "turnover_ntd": number(x.get(val_c)),
        })
    return pd.DataFrame(rows)


def main():
    frames = []
    errors = []
    for name, fn in [("TWSE", fetch_twse), ("TPEx", fetch_tpex)]:
        try:
            part = fn()
            if not part.empty:
                frames.append(part)
                print(f"{name}: {len(part)} 檔")
        except Exception as exc:
            errors.append(f"{name}: {exc}")
            print(f"WARNING {name}: {exc}")

    if not frames:
        raise RuntimeError("TWSE / TPEx 均未取得資料: " + " | ".join(errors))

    today = pd.concat(frames, ignore_index=True)
    today = today.dropna(subset=["close", "volume_shares"])
    out = DATA / "market_data.csv"
    if out.exists():
        old = pd.read_csv(out, dtype={"stock_id": str})
        all_data = pd.concat([old, today], ignore_index=True)
        all_data = all_data.drop_duplicates(["date", "stock_id"], keep="last")
    else:
        all_data = today
    all_data.sort_values(["date", "stock_id"]).to_csv(out, index=False, encoding="utf-8-sig")

    master = today[["stock_id", "stock_name", "market"]].drop_duplicates("stock_id")
    master.to_csv(DATA / "stock_master.csv", index=False, encoding="utf-8-sig")
    print(f"market_data 累計 {len(all_data)} 列；今日 {len(today)} 檔")
    if errors:
        print("部分來源警告: " + " | ".join(errors))


if __name__ == "__main__":
    main()

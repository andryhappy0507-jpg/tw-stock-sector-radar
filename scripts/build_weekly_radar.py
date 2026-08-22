from pathlib import Path
import pandas as pd

DATA = Path("data")
OUT = DATA / "weekly_signal.csv"
SCREEN_OUT = DATA / "weekly_screen.csv"
SUMMARY_OUT = DATA / "weekly_summary.csv"


def main():
    path = DATA / "market_data.csv"
    if not path.exists():
        print("market_data.csv 尚未產生，先略過週雷達計算")
        return

    df = pd.read_csv(path, dtype={"stock_id": str}, parse_dates=["date"])
    required = {"date", "stock_id", "close", "volume_shares", "turnover_ntd"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"market_data.csv 缺少欄位: {sorted(missing)}")

    df = df.sort_values(["stock_id", "date"])
    g = df.groupby("stock_id", group_keys=False)
    df["prev_close_5"] = g["close"].shift(5)
    df["weekly_return_pct"] = (df["close"] / df["prev_close_5"] - 1) * 100
    df["avg_volume_5"] = g["volume_shares"].transform(lambda s: s.rolling(5).mean())
    df["avg_volume_prev20"] = g["volume_shares"].transform(lambda s: s.shift(5).rolling(20).mean())
    df["volume_ratio"] = df["avg_volume_5"] / df["avg_volume_prev20"]
    df["avg_turnover_5"] = g["turnover_ntd"].transform(lambda s: s.rolling(5).mean())
    df["avg_turnover_prev20"] = g["turnover_ntd"].transform(lambda s: s.shift(5).rolling(20).mean())
    df["turnover_ratio"] = df["avg_turnover_5"] / df["avg_turnover_prev20"]

    latest = df.groupby("stock_id", as_index=False).tail(1).copy()
    latest["price_strong"] = latest["weekly_return_pct"] >= 5
    latest["volume_strong"] = latest["volume_ratio"] >= 1.5
    latest["liquid"] = latest["avg_volume_5"] >= 1_000_000  # 1,000 張 = 1,000,000 股

    master = DATA / "stock_master.csv"
    if master.exists():
        latest = latest.merge(pd.read_csv(master, dtype={"stock_id": str}), on="stock_id", how="left")

    latest.to_csv(OUT, index=False, encoding="utf-8-sig")

    # 第一階段分析：全部週漲幅 >= 5% 個股，不先限縮為前 N 名。
    screen = latest[latest["price_strong"]].copy()
    screen["price_and_volume_strong"] = screen["price_strong"] & screen["volume_strong"]
    screen = screen.sort_values(["price_and_volume_strong", "weekly_return_pct", "volume_ratio"], ascending=[False, False, False])
    screen.to_csv(SCREEN_OUT, index=False, encoding="utf-8-sig")

    latest_date = latest["date"].max()
    summary = pd.DataFrame([{
        "latest_date": latest_date.date().isoformat() if pd.notna(latest_date) else "",
        "stocks_total": int(len(latest)),
        "price_ge_5pct": int(latest["price_strong"].sum()),
        "volume_ge_1_5x": int(latest["volume_strong"].sum()),
        "price_ge_5pct_and_volume_ge_1_5x": int((latest["price_strong"] & latest["volume_strong"]).sum()),
        "price_ge_5pct_and_liquid": int((latest["price_strong"] & latest["liquid"]).sum()),
    }])
    summary.to_csv(SUMMARY_OUT, index=False, encoding="utf-8-sig")

    print(f"輸出 {OUT}: {len(latest)} 檔")
    print(f"週漲幅 >= 5%: {len(screen)} 檔，其中量增 >= 1.5x: {int(screen['volume_strong'].sum())} 檔")


if __name__ == "__main__":
    main()

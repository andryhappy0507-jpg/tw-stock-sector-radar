from pathlib import Path
import pandas as pd

DATA = Path("data")
OUT = DATA / "weekly_signal.csv"


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
    print(f"輸出 {OUT}: {len(latest)} 檔")


if __name__ == "__main__":
    main()

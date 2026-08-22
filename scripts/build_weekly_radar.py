from pathlib import Path
import pandas as pd

DATA = Path("data")
OUT = DATA / "weekly_signal.csv"
SCREEN_OUT = DATA / "weekly_screen.csv"
SUMMARY_OUT = DATA / "weekly_summary.csv"
PREV_OUT = DATA / "previous_week_signal.csv"


def enrich(df):
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
    return df


def snapshot_for_date(df, target_date):
    snap = df[df["date"] <= target_date].groupby("stock_id", as_index=False).tail(1).copy()
    snap["price_strong"] = snap["weekly_return_pct"] >= 5
    snap["volume_strong"] = snap["volume_ratio"] >= 1.5
    snap["liquid"] = snap["avg_volume_5"] >= 1_000_000
    snap["abc_group"] = ""
    snap.loc[snap["price_strong"] & snap["volume_strong"] & snap["liquid"], "abc_group"] = "A"
    snap.loc[snap["price_strong"] & ~((snap["volume_strong"]) & (snap["liquid"])), "abc_group"] = "B"
    snap.loc[(~snap["price_strong"]) & snap["volume_strong"] & snap["liquid"], "abc_group"] = "C"
    return snap


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

    df = enrich(df)
    dates = sorted(df["date"].dropna().unique())
    latest_date = pd.Timestamp(dates[-1])
    previous_target = latest_date - pd.Timedelta(days=7)
    previous_date = max(pd.Timestamp(d) for d in dates if pd.Timestamp(d) <= previous_target)

    latest = snapshot_for_date(df, latest_date)
    previous = snapshot_for_date(df, previous_date)

    master = DATA / "stock_master.csv"
    if master.exists():
        m = pd.read_csv(master, dtype={"stock_id": str})
        latest = latest.merge(m, on="stock_id", how="left")
        previous = previous.merge(m, on="stock_id", how="left")

    latest.to_csv(OUT, index=False, encoding="utf-8-sig")
    previous.to_csv(PREV_OUT, index=False, encoding="utf-8-sig")

    screen = latest[latest["price_strong"]].copy().sort_values(["weekly_return_pct", "volume_ratio"], ascending=[False, False])
    screen.to_csv(SCREEN_OUT, index=False, encoding="utf-8-sig")

    summary = pd.DataFrame([{
        "latest_date": latest_date.date().isoformat(),
        "previous_week_date": previous_date.date().isoformat(),
        "stocks_total": int(len(latest)),
        "price_ge_5pct": int(latest["price_strong"].sum()),
        "volume_ge_1_5x": int(latest["volume_strong"].sum()),
        "A_count": int((latest["abc_group"] == "A").sum()),
        "B_count": int((latest["abc_group"] == "B").sum()),
        "C_count": int((latest["abc_group"] == "C").sum()),
        "prev_A_count": int((previous["abc_group"] == "A").sum()),
        "prev_B_count": int((previous["abc_group"] == "B").sum()),
        "prev_C_count": int((previous["abc_group"] == "C").sum()),
    }])
    summary.to_csv(SUMMARY_OUT, index=False, encoding="utf-8-sig")
    print(f"本週 {latest_date.date()}；上週基準 {previous_date.date()}")
    print(f"上週 ABC: A={(previous['abc_group']=='A').sum()} B={(previous['abc_group']=='B').sum()} C={(previous['abc_group']=='C').sum()}")


if __name__ == "__main__":
    main()

import warnings
warnings.filterwarnings("ignore", message=".*inplace.*")
import os
import yfinance as yf
import pandas as pd

# The assets we track: Yahoo Finance symbol -> readable name
ASSETS = {
    "BTC-USD": "Bitcoin",
    "ETH-USD": "Ethereum",
    "GC=F": "Gold",
    "EURUSD=X": "EUR/USD",
    "AAPL": "Apple",
}


def fetch_prices(period="30d"):
    frames = []
    for symbol, name in ASSETS.items():
        df = yf.Ticker(symbol).history(period=period, interval="1d")
        if df.empty:
            print(f"No data returned for {symbol}")
            continue
        df = df.reset_index()
        df["Date"] = df["Date"].dt.tz_localize(None)
        df["asset"] = symbol
        df["asset_name"] = name
        frames.append(df)

    if not frames:
        raise RuntimeError("No data fetched for any asset")

    data = pd.concat(frames, ignore_index=True)

    data = data.rename(columns={
        "Date": "price_date",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume",
    })
    data["price_date"] = pd.to_datetime(data["price_date"]).dt.date
    data["loaded_at"] = pd.Timestamp.now()

    return data[["asset", "asset_name", "price_date", "open", "high", "low", "close", "volume", "loaded_at"]]


if __name__ == "__main__":
    prices = fetch_prices()
    print(prices.head(10))
    print(f"\nTotal rows: {len(prices)}")

    os.makedirs("data", exist_ok=True)
    prices.to_csv("data/raw_prices.csv", index=False)
    print("Saved to data/raw_prices.csv")
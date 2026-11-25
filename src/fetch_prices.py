import pandas as pd
import yfinance as yf

SYMBOLS = ["AAPL", "MSFT", "NVDA", "^GSPC",
           "BTC-USD", "ETH-USD", "EURUSD=X", "GC=F"]

def fetch_prices(symbols, period="1mo"):
    frames = []
    for symbol in symbols:
        df = yf.Ticker(symbol).history(period=period).reset_index()
        df["Date"] = df["Date"].dt.date   # plain date, timezone dropped
        df["symbol"] = symbol
        frames.append(df)
    data = pd.concat(frames, ignore_index=True)
    data = data.rename(columns={
        "Date": "date", "Open": "open", "High": "high",
        "Low": "low", "Close": "close", "Volume": "volume",
    })
    return data[["symbol", "date", "open", "high", "low", "close", "volume"]]

if __name__ == "__main__":
    prices = fetch_prices(SYMBOLS)
    print(prices.head(10))
    print(prices.groupby("symbol").size())
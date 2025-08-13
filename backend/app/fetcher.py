import yfinance as yf
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime, timezone

load_dotenv()
DB_URL = os.getenv("DATABASE_URL", f"postgresql+psycopg2://sgf_user:sgf_pass@localhost:5432/signalforge")
engine = create_engine(DB_URL, future=True)

def store_prices(symbol: str, df: pd.DataFrame):
    # df index is DatetimeIndex in UTC; convert to tz-aware ts column
    df["Datetime"] = pd.to_datetime(df["Datetime"], errors="coerce")
    df = df.set_index("Datetime")
    df = df.tz_localize(None).reset_index()  # remove tz info for SQL insertion
    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(text(
                "INSERT INTO prices (symbol, ts, open, high, low, close, volume) VALUES "
                "(:sym, :ts, :o, :h, :l, :c, :v) ON CONFLICT DO NOTHING"
            ), {
                "sym": symbol.upper(),
                "ts": row['Datetime'].to_pydatetime(),
                "o": float(row['Open']),
                "h": float(row['High']),
                "l": float(row['Low']),
                "c": float(row['Close']),
                "v": int(row['Volume'])
            })

def fetch_and_store(symbol="MSFT", period="60d", interval="1d"):
    print(f"Fetching {symbol}")
    t = yf.Ticker(symbol)
    df = t.history(period=period, interval=interval)
    if df.empty:
        print("No data")
        return
    # yfinance returns index tz-aware; reset index
    df = df.reset_index().rename(columns={"index":"Datetime"})
    # ensure datetime column exists
    if 'Datetime' not in df.columns:
        df['Datetime'] = df.index
    # normalizing
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    print(df.head())
    # select columns
    store_prices(symbol, df[['cfr', 'Open', 'High', 'Low', 'Close', 'Volume']])

if __name__ == "__main__":
    # example: fetch for multiple tickers
    for sym in ["MSFT", "AAPL", "GOOG"]:
        fetch_and_store(sym, period="60d", interval="1d")
    
    print("Data fetching complete.")

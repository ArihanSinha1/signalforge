# SignalForge Backend API
# Provides access to stock price data and health check endpoint


from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

app = FastAPI(title="SignalForge Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = create_engine(DB_URL, future=True)

@app.get("/api/health")
def health():
    return {"ok": True}

@app.get("/api/prices")
def get_prices(symbol: str = "MSFT", limit: int = 100):
    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT ts, open, high, low, close, volume FROM prices WHERE symbol = :sym ORDER BY ts DESC LIMIT :lim"),
            {"sym": symbol.upper(), "lim": limit}
        ).fetchall()
    # return newest-to-oldest reversed to chronological
    rows = [dict(ts=r[0].isoformat(), open=r[1], high=r[2], low=r[3], close=r[4], volume=r[5]) for r in reversed(rows)]
    return {"symbol": symbol.upper(), "prices": rows}

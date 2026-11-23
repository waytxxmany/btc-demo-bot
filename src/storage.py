import os
import sqlite3
from contextlib import closing
from datetime import datetime

from src.parser import Quote


DEFAULT_DB_PATH = "data/quotes.db"

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS quotes (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    ts     TEXT NOT NULL,
    price  REAL NOT NULL,
    UNIQUE (symbol, ts)
)
"""


def _connect(db_path: str) -> sqlite3.Connection:
    folder = os.path.dirname(db_path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    return sqlite3.connect(db_path)


def init_db(db_path: str = DEFAULT_DB_PATH) -> None:
    with closing(_connect(db_path)) as conn:
        with conn:
            conn.execute(CREATE_TABLE)


def save_quote(quote: Quote, db_path: str = DEFAULT_DB_PATH) -> bool:
    with closing(_connect(db_path)) as conn:
        with conn:
            cur = conn.execute(
                "INSERT OR IGNORE INTO quotes (symbol, ts, price) VALUES (?, ?, ?)",
                (quote.symbol, quote.ts.isoformat(), quote.price),
            )
            inserted = cur.rowcount == 1
    return inserted


def get_history(symbol: str, limit: int = 10, db_path: str = DEFAULT_DB_PATH) -> list[Quote]:
    with closing(_connect(db_path)) as conn:
        rows = conn.execute(
            "SELECT symbol, ts, price FROM quotes WHERE symbol = ? ORDER BY ts DESC LIMIT ?",
            (symbol, limit),
        ).fetchall()
    return [Quote(symbol=s, price=p, ts=datetime.fromisoformat(t)) for s, t, p in rows]


def get_latest(symbol: str, db_path: str = DEFAULT_DB_PATH) -> Quote | None:
    history = get_history(symbol, limit=1, db_path=db_path)
    return history[0] if history else None

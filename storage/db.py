# storage/db.py
import sqlite3
from datetime import datetime

DB_PATH = "traffic.db"


def _connect():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = _connect()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS crossings (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            label     TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def record_crossing(label):
    conn = _connect()
    conn.execute(
        "INSERT INTO crossings (timestamp, label) VALUES (?, ?)",
        (datetime.now().isoformat(), label),
    )
    conn.commit()
    conn.close()


def get_counts_per_minute():
    conn = _connect()
    rows = conn.execute("""
        SELECT strftime('%Y-%m-%d %H:%M', timestamp) AS minute,
               COUNT(*) AS count
        FROM crossings
        GROUP BY minute
        ORDER BY minute
    """).fetchall()
    conn.close()
    return rows
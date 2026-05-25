"""
SQLite-basert cache for API-responser.
Nøkkel/verdi-cache med TTL (time-to-live) i sekunder.
"""
import sqlite3
import json
import time
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cache.db")


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cache (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            expires_at REAL NOT NULL
        )
    """)
    conn.commit()
    return conn


def get(key: str) -> dict | list | None:
    with _conn() as conn:
        row = conn.execute(
            "SELECT value, expires_at FROM cache WHERE key = ?", (key,)
        ).fetchone()
        if row and row[1] > time.time():
            return json.loads(row[0])
        return None


def set(key: str, value: dict | list, ttl: int = 3600) -> None:
    with _conn() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO cache (key, value, expires_at) VALUES (?, ?, ?)",
            (key, json.dumps(value), time.time() + ttl)
        )


def invalidate(key: str) -> None:
    with _conn() as conn:
        conn.execute("DELETE FROM cache WHERE key = ?", (key,))


def clear_expired() -> int:
    with _conn() as conn:
        cursor = conn.execute("DELETE FROM cache WHERE expires_at <= ?", (time.time(),))
        return cursor.rowcount

from __future__ import annotations

import sqlite3
from pathlib import Path


DB_PATH = Path("data/stock_state.db")


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS stock_state (
                item_code TEXT NOT NULL,
                store_code TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (item_code, store_code)
            )
            """
        )


def get_previous_quantity(item_code: str, store_code: str) -> int | None:
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            """
            SELECT quantity
            FROM stock_state
            WHERE item_code = ?
              AND store_code = ?
            """,
            (item_code, store_code),
        ).fetchone()

    return row[0] if row else None


def save_quantity(item_code: str, store_code: str, quantity: int) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO stock_state (item_code, store_code, quantity)
            VALUES (?, ?, ?)
            ON CONFLICT(item_code, store_code)
            DO UPDATE SET
                quantity = excluded.quantity,
                updated_at = CURRENT_TIMESTAMP
            """,
            (item_code, store_code, quantity),
        )

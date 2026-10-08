# 1_DATA/database.py — SQLite 数据访问

import sqlite3
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
import config  # noqa: E402


def get_connection() -> sqlite3.Connection:
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_schema() -> None:
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS platforms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            );
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform_id INTEGER,
                keyword TEXT,
                title TEXT,
                price REAL,
                want_count INTEGER,
                view_count INTEGER,
                comment_count INTEGER DEFAULT 0,
                share_count INTEGER DEFAULT 0,
                seller TEXT,
                tags TEXT,
                publish_time TEXT,
                source_url TEXT,
                raw_json TEXT,
                collect_date TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS keywords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT UNIQUE NOT NULL,
                category TEXT,
                first_seen_date TEXT,
                last_seen_date TEXT,
                is_sensitive INTEGER DEFAULT 0,
                is_low_efficiency INTEGER DEFAULT 0,
                last_search_date TEXT
            );
            CREATE TABLE IF NOT EXISTS collection_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_date TEXT NOT NULL,
                platform_id INTEGER,
                keyword TEXT,
                total_items INTEGER DEFAULT 0,
                valid_items INTEGER DEFAULT 0,
                status TEXT DEFAULT 'running',
                started_at TEXT,
                finished_at TEXT
            );
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                hot_score REAL,
                trend_score REAL,
                comp_score REAL,
                profit_score REAL,
                difficulty_score REAL,
                total_score REAL,
                scored_date TEXT NOT NULL
            );
            """
        )
        conn.execute(
            "INSERT OR IGNORE INTO platforms (id, name) VALUES (1, 'xianyu')"
        )
        conn.commit()


def upsert_keyword(keyword: str, category: str = "default") -> None:
    today = date.today().isoformat()
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id FROM keywords WHERE keyword = ?", (keyword,)
        ).fetchone()
        if row:
            conn.execute(
                "UPDATE keywords SET last_seen_date=?, last_search_date=? WHERE keyword=?",
                (today, today, keyword),
            )
        else:
            conn.execute(
                """INSERT INTO keywords (keyword, category, first_seen_date, last_seen_date, last_search_date)
                   VALUES (?, ?, ?, ?, ?)""",
                (keyword, category, today, today, today),
            )
        conn.commit()


def insert_product(row: dict) -> int:
    cols = [
        "platform_id", "keyword", "title", "price", "want_count", "view_count",
        "comment_count", "share_count", "seller", "tags", "publish_time",
        "source_url", "raw_json", "collect_date",
    ]
    values = [row.get(c) for c in cols]
    with get_connection() as conn:
        cur = conn.execute(
            f"INSERT INTO products ({', '.join(cols)}) VALUES ({', '.join('?' * len(cols))})",
            values,
        )
        conn.commit()
        return cur.lastrowid


def start_collection_log(keyword: str, platform_id: int = 1) -> int:
    from datetime import datetime

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today = date.today().isoformat()
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO collection_log (task_date, platform_id, keyword, status, started_at)
               VALUES (?, ?, ?, 'running', ?)""",
            (today, platform_id, keyword, now),
        )
        conn.commit()
        return cur.lastrowid


def finish_collection_log(log_id: int, total: int, valid: int, status: str = "done") -> None:
    from datetime import datetime

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        conn.execute(
            """UPDATE collection_log SET total_items=?, valid_items=?, status=?, finished_at=?
               WHERE id=?""",
            (total, valid, status, now, log_id),
        )
        conn.commit()


def get_products_by_keyword(keyword: str, limit: int = 50) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT * FROM products WHERE keyword = ? ORDER BY id DESC LIMIT ?""",
            (keyword, limit),
        ).fetchall()
    return [dict(r) for r in rows]


def save_score(product_id: int, scores: dict, scored_date: str | None = None) -> None:
    scored_date = scored_date or date.today().isoformat()
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO scores
               (product_id, hot_score, trend_score, comp_score, profit_score,
                difficulty_score, total_score, scored_date)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                product_id,
                scores["hot"],
                scores["trend"],
                scores["comp"],
                scores["profit"],
                scores["difficulty"],
                scores["total"],
                scored_date,
            ),
        )
        conn.commit()


def get_top_scored_products(keyword: str, limit: int = 5) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT p.*, s.total_score, s.hot_score, s.profit_score
            FROM products p
            JOIN scores s ON s.product_id = p.id
            WHERE p.keyword = ?
            ORDER BY s.total_score DESC
            LIMIT ?
            """,
            (keyword, limit),
        ).fetchall()
    return [dict(r) for r in rows]

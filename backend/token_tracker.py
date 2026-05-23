"""Persistent token usage tracker via SQLite."""
import aiosqlite
import time
import os
from typing import Optional

DB_PATH = os.getenv("DATABASE_URL", "sqlite:///./testforge.db").replace("sqlite:///", "")

SCHEMA = """
CREATE TABLE IF NOT EXISTS token_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp REAL NOT NULL,
    agent TEXT NOT NULL,
    job_id TEXT NOT NULL,
    prompt_tokens INTEGER NOT NULL DEFAULT 0,
    completion_tokens INTEGER NOT NULL DEFAULT 0,
    total_tokens INTEGER NOT NULL DEFAULT 0,
    model TEXT NOT NULL DEFAULT ''
);
"""


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(SCHEMA)
        await db.commit()


async def record_usage(agent: str, job_id: str, prompt_tokens: int, completion_tokens: int, model: str = ""):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO token_usage (timestamp, agent, job_id, prompt_tokens, completion_tokens, total_tokens, model) VALUES (?,?,?,?,?,?,?)",
            (time.time(), agent, job_id, prompt_tokens, completion_tokens, prompt_tokens + completion_tokens, model),
        )
        await db.commit()


async def get_stats() -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        rows = await db.execute_fetchall("""
            SELECT agent, 
                   COUNT(*) as calls, 
                   SUM(prompt_tokens) as total_prompt,
                   SUM(completion_tokens) as total_completion,
                   SUM(total_tokens) as total
            FROM token_usage GROUP BY agent ORDER BY total DESC
        """)
        agents = [dict(r) for r in rows]

        total_row = await db.execute_fetchall("SELECT SUM(total_tokens) as grand_total, COUNT(*) as total_calls FROM token_usage")
        t = dict(total_row[0]) if total_row else {}
        return {
            "agents": agents,
            "grand_total_tokens": t.get("grand_total", 0) or 0,
            "total_api_calls": t.get("total_calls", 0) or 0,
        }

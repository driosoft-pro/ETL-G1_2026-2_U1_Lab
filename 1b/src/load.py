"""
Load module - export data to CSV and SQLite database.
"""
import os
import sqlite3
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DB_PATH = Path(os.getenv("DB_PATH", "data/retail_analytics.db"))


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """Get a SQLite connection."""
    return sqlite3.connect(str(db_path))


def load_to_csv(df: pd.DataFrame, output_path: Path) -> None:
    """Export integrated data to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


def load_to_sqlite(df: pd.DataFrame, table_name: str = "sales_analytics",
                   db_path: Path = DB_PATH) -> None:
    """Load data into SQLite database."""
    conn = get_connection(db_path)
    try:
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {table_name}")
        df.to_sql(table_name, conn, if_exists="append", index=False)
        conn.commit()
    finally:
        conn.close()


def create_tables(db_path: Path = DB_PATH) -> None:
    """Create tables in SQLite database."""
    from database.init_sqlite import init_database
    init_database(db_path)

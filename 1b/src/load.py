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


def load_references_to_sqlite(references: dict, db_path: Path = DB_PATH) -> None:
    """Load reference tables (products, stores, promotions, targets) into SQLite."""
    table_map = {
        "products": "products",
        "stores": "stores",
        "promotions": "promotions",
        "targets": "monthly_targets",
    }
    conn = get_connection(db_path)
    try:
        for key, table_name in table_map.items():
            if key in references:
                df = references[key]
                cur = conn.cursor()
                cur.execute(f"DELETE FROM {table_name}")
                df.to_sql(table_name, conn, if_exists="append", index=False)
                print(f"  Loaded {len(df)} rows into {table_name}")
        conn.commit()
    finally:
        conn.close()


def create_tables(db_path: Path = DB_PATH) -> None:
    """Create tables in SQLite database."""
    from database.init_sqlite import init_database
    init_database(db_path)


def create_vanilla_database(raw_data: dict, db_path: Path) -> None:
    """Create vanilla_analytics.db with raw data (no cleaning, no treatment)."""
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    try:
        cur = conn.cursor()

        cur.execute("DROP TABLE IF EXISTS sales_raw")
        cur.execute("DROP TABLE IF EXISTS products")
        cur.execute("DROP TABLE IF EXISTS stores")
        cur.execute("DROP TABLE IF EXISTS promotions")
        cur.execute("DROP TABLE IF EXISTS monthly_targets")

        cur.execute("""
            CREATE TABLE IF NOT EXISTS sales_raw (
                sale_line_id TEXT,
                sale_date TEXT,
                store_id TEXT,
                product_id TEXT,
                quantity TEXT,
                unit_price TEXT,
                promotion_code TEXT,
                payment_method TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id TEXT,
                product_name TEXT,
                category TEXT,
                list_price TEXT,
                unit_cost TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS stores (
                store_id TEXT,
                store_name TEXT,
                city TEXT,
                region TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS promotions (
                promotion_code TEXT,
                product_id TEXT,
                start_date TEXT,
                end_date TEXT,
                discount_pct TEXT,
                campaign_name TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS monthly_targets (
                store_id TEXT,
                month TEXT,
                sales_target TEXT
            )
        """)

        conn.commit()

        transactions = raw_data["transactions"].copy()
        transactions.columns = [c.strip().lower() for c in transactions.columns]
        for col in transactions.columns:
            transactions[col] = transactions[col].astype(str).str.strip()
        transactions.to_sql("sales_raw", conn, if_exists="append", index=False)
        print(f"  Loaded {len(transactions)} rows into sales_raw")

        for key, table_name in [("products", "products"), ("stores", "stores"),
                                 ("promotions", "promotions"), ("targets", "monthly_targets")]:
            if key in raw_data:
                df = raw_data[key].copy()
                df.columns = [c.strip().lower() for c in df.columns]
                for col in df.columns:
                    df[col] = df[col].astype(str).str.strip()
                df.to_sql(table_name, conn, if_exists="append", index=False)
                print(f"  Loaded {len(df)} rows into {table_name}")

        conn.commit()
    finally:
        conn.close()

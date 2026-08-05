"""
SQLite database initialization.
Creates the retail analytics schema in a local SQLite database.
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "retail_analytics.db"


def init_database(db_path: Path = DB_PATH) -> None:
    """Create all tables and indexes for the retail analytics database."""
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    try:
        cur = conn.cursor()

        cur.execute("DROP TABLE IF EXISTS sales_analytics")
        cur.execute("DROP TABLE IF EXISTS monthly_targets")
        cur.execute("DROP TABLE IF EXISTS promotions")
        cur.execute("DROP TABLE IF EXISTS stores")
        cur.execute("DROP TABLE IF EXISTS products")

        cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id TEXT PRIMARY KEY,
                product_name TEXT NOT NULL,
                category TEXT,
                list_price REAL,
                unit_cost REAL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS stores (
                store_id TEXT PRIMARY KEY,
                store_name TEXT NOT NULL,
                city TEXT,
                region TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS promotions (
                promotion_code TEXT PRIMARY KEY,
                product_id TEXT,
                start_date TEXT,
                end_date TEXT,
                discount_pct REAL,
                campaign_name TEXT,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS monthly_targets (
                store_id TEXT,
                month TEXT,
                sales_target REAL,
                PRIMARY KEY (store_id, month),
                FOREIGN KEY (store_id) REFERENCES stores(store_id)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS sales_analytics (
                sale_line_id TEXT PRIMARY KEY,
                sale_date TEXT NOT NULL,
                store_id TEXT,
                store_name TEXT,
                city TEXT,
                region TEXT,
                product_id TEXT,
                product_name TEXT,
                category TEXT,
                quantity INTEGER,
                unit_price REAL,
                promotion_code TEXT,
                campaign_name TEXT,
                discount_pct REAL,
                payment_method TEXT,
                gross_sales REAL,
                discount_amount REAL,
                net_sales REAL,
                sales_target REAL,
                month TEXT,
                week INTEGER,
                day_name TEXT,
                FOREIGN KEY (store_id) REFERENCES stores(store_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        """)

        cur.execute("CREATE INDEX IF NOT EXISTS idx_sales_date ON sales_analytics(sale_date)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_sales_store ON sales_analytics(store_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_sales_product ON sales_analytics(product_id)")

        conn.commit()
        print(f"Database initialized at {db_path}")
    finally:
        conn.close()


if __name__ == "__main__":
    init_database()

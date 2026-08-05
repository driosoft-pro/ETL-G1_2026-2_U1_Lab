"""
Tests for load module.
"""
import pytest
import sqlite3
import pandas as pd
from pathlib import Path
from src.load import load_to_csv, load_to_sqlite, create_tables, get_connection

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DB_PATH = DATA_DIR / "test.db"


@pytest.fixture(autouse=True)
def setup_db():
    create_tables(DB_PATH)
    yield
    if DB_PATH.exists():
        DB_PATH.unlink()


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "sale_line_id": ["LTEST01", "LTEST02"],
        "sale_date": ["2026-02-01", "2026-03-15"],
        "store_id": ["S01", "S02"],
        "store_name": ["Cali Norte", "Bogota Centro"],
        "city": ["Cali", "Bogota"],
        "region": ["Southwest", "Central"],
        "product_id": ["P001", "P002"],
        "product_name": ["Coffee Maker Basic", "Coffee Maker Premium"],
        "category": ["Small Appliances", "Small Appliances"],
        "quantity": [2, 1],
        "unit_price": [145000, 285000],
        "promotion_code": ["", ""],
        "campaign_name": ["", ""],
        "discount_pct": [0.0, 0.0],
        "payment_method": ["Card", "Cash"],
        "gross_sales": [290000, 285000],
        "discount_amount": [0.0, 0.0],
        "net_sales": [290000, 285000],
        "sales_target": [19500000, 23000000],
        "month": ["2026-02", "2026-03"],
        "week": [5, 11],
        "day_name": ["Sunday", "Saturday"],
    })


class TestLoadCSV:
    def test_creates_csv(self, sample_df):
        output = DATA_DIR / "processed" / "test_output.csv"
        load_to_csv(sample_df, output)
        assert output.exists()
        loaded = pd.read_csv(output)
        assert len(loaded) == 2
        output.unlink()


class TestLoadSQLite:
    def test_loads_to_db(self, sample_df):
        load_to_sqlite(sample_df, "sales_analytics", DB_PATH)
        conn = sqlite3.connect(str(DB_PATH))
        df = pd.read_sql_query("SELECT COUNT(*) as cnt FROM sales_analytics", conn)
        assert df["cnt"].iloc[0] == 2
        conn.close()

    def test_replaces_existing(self, sample_df):
        load_to_sqlite(sample_df, "sales_analytics", DB_PATH)
        load_to_sqlite(sample_df, "sales_analytics", DB_PATH)
        conn = sqlite3.connect(str(DB_PATH))
        df = pd.read_sql_query("SELECT COUNT(*) as cnt FROM sales_analytics", conn)
        assert df["cnt"].iloc[0] == 2
        conn.close()


class TestCreateTables:
    def test_creates_db_file(self):
        assert DB_PATH.exists()

    def test_creates_sales_analytics(self):
        conn = sqlite3.connect(str(DB_PATH))
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sales_analytics'")
        assert cur.fetchone() is not None
        conn.close()

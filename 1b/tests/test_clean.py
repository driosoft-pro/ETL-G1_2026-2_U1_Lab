"""
Tests for clean module.
"""
import pytest
import pandas as pd
from src.clean import clean_transactions, clean_references
from src.extract import extract_all
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


@pytest.fixture
def raw_data():
    return extract_all(DATA_DIR)


class TestCleanTransactions:
    def test_removes_duplicates(self, raw_data):
        df = raw_data["transactions"]
        cleaned = clean_transactions(df)
        assert cleaned["sale_line_id"].is_unique

    def test_removes_invalid_quantity(self, raw_data):
        cleaned = clean_transactions(raw_data["transactions"])
        assert (cleaned["quantity"] > 0).all()

    def test_removes_invalid_price(self, raw_data):
        cleaned = clean_transactions(raw_data["transactions"])
        assert (cleaned["unit_price"] > 0).all()

    def test_dates_converted(self, raw_data):
        cleaned = clean_transactions(raw_data["transactions"])
        assert pd.api.types.is_datetime64_any_dtype(cleaned["sale_date"])

    def test_numeric_types(self, raw_data):
        cleaned = clean_transactions(raw_data["transactions"])
        assert pd.api.types.is_numeric_dtype(cleaned["quantity"])
        assert pd.api.types.is_numeric_dtype(cleaned["unit_price"])

    def test_no_null_ids(self, raw_data):
        cleaned = clean_transactions(raw_data["transactions"])
        assert cleaned["sale_line_id"].notna().all()
        assert cleaned["store_id"].notna().all()
        assert cleaned["product_id"].notna().all()


class TestCleanReferences:
    def test_returns_all_tables(self, raw_data):
        refs = clean_references(
            raw_data["products"], raw_data["stores"],
            raw_data["promotions"], raw_data["targets"]
        )
        assert "products" in refs
        assert "stores" in refs
        assert "promotions" in refs
        assert "targets" in refs

    def test_columns_lowercased(self, raw_data):
        refs = clean_references(
            raw_data["products"], raw_data["stores"],
            raw_data["promotions"], raw_data["targets"]
        )
        for df in refs.values():
            assert all(c == c.lower() for c in df.columns)

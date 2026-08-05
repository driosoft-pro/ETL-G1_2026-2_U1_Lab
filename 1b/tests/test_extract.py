"""
Tests for extract module.
"""
import pytest
from pathlib import Path
from src.extract import extract_csv, extract_json, extract_xml, extract_all

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


class TestExtractCSV:
    def test_extract_transactions(self):
        df = extract_csv(DATA_DIR / "sales_cali.csv")
        assert not df.empty
        assert "sale_line_id" in df.columns
        assert "sale_date" in df.columns

    def test_extract_products(self):
        df = extract_csv(DATA_DIR / "products.csv")
        assert not df.empty
        assert "product_id" in df.columns
        assert "product_name" in df.columns

    def test_extract_stores(self):
        df = extract_csv(DATA_DIR / "stores.csv")
        assert len(df) == 3


class TestExtractJSON:
    def test_extract_bogota(self):
        df = extract_json(DATA_DIR / "sales_bogota.json")
        assert not df.empty
        assert "sale_line_id" in df.columns
        assert "sale_date" in df.columns
        assert df["store_id"].unique()[0] == "S02"


class TestExtractXML:
    def test_extract_medellin(self):
        df = extract_xml(DATA_DIR / "sales_medellin.xml")
        assert not df.empty
        assert "sale_line_id" in df.columns
        assert df["store_id"].unique()[0] == "S03"


class TestExtractAll:
    def test_returns_all_datasets(self):
        result = extract_all(DATA_DIR)
        assert "transactions" in result
        assert "products" in result
        assert "stores" in result
        assert "promotions" in result
        assert "targets" in result

    def test_transactions_combined(self):
        result = extract_all(DATA_DIR)
        assert len(result["transactions"]) > 500

    def test_schema_unified(self):
        result = extract_all(DATA_DIR)
        expected_cols = {
            "sale_line_id", "sale_date", "store_id", "product_id",
            "quantity", "unit_price", "promotion_code", "payment_method"
        }
        assert set(result["transactions"].columns) == expected_cols

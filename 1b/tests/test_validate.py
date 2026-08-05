"""
Tests for validate module.
"""
import pytest
import pandas as pd
from src.extract import extract_all
from src.clean import clean_transactions, clean_references
from src.transform import transform_all
from src.validate import (
    validate_unique_ids, validate_foreign_keys,
    validate_positive_sales, validate_formulas, validate_all
)
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


@pytest.fixture
def integrated_data():
    raw = extract_all(DATA_DIR)
    cleaned_tx = clean_transactions(raw["transactions"])
    refs = clean_references(
        raw["products"], raw["stores"],
        raw["promotions"], raw["targets"]
    )
    integrated = transform_all(
        cleaned_tx, refs["products"], refs["stores"],
        refs["promotions"], refs["targets"]
    )
    return integrated, refs


class TestValidateUniqueIds:
    def test_unique_ids(self, integrated_data):
        df, _ = integrated_data
        assert validate_unique_ids(df)

    test_data = pd.DataFrame({
        "sale_line_id": ["L001", "L001", "L002"],
        "other": [1, 2, 3]
    })

    def test_duplicate_ids(self):
        assert not validate_unique_ids(self.test_data)


class TestValidateForeignKeys:
    def test_valid_keys(self, integrated_data):
        df, refs = integrated_data
        assert validate_foreign_keys(df, refs)


class TestValidatePositiveSales:
    def test_positive_values(self, integrated_data):
        df, _ = integrated_data
        assert validate_positive_sales(df)

    test_data = pd.DataFrame({
        "quantity": [1, -1, 2],
        "unit_price": [100, 200, 300],
        "gross_sales": [100, -200, 600],
        "net_sales": [100, -200, 600]
    })

    def test_negative_values(self):
        assert not validate_positive_sales(self.test_data)


class TestValidateFormulas:
    def test_correct_formulas(self, integrated_data):
        df, _ = integrated_data
        assert validate_formulas(df)

    test_data = pd.DataFrame({
        "gross_sales": [100, 200],
        "discount_amount": [10, 20],
        "net_sales": [90, 180]
    })

    def test_incorrect_formulas(self):
        bad = self.test_data.copy()
        bad.loc[0, "net_sales"] = 999
        assert not validate_formulas(bad)


class TestValidateAll:
    def test_passes(self, integrated_data):
        df, refs = integrated_data
        result = validate_all(df, refs)
        assert result["passed"]
        assert len(result["errors"]) == 0

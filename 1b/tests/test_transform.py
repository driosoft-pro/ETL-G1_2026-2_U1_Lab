"""
Tests for transform module.
"""
import pytest
import pandas as pd
from src.extract import extract_all
from src.clean import clean_transactions, clean_references
from src.transform import (
    integrate_products, integrate_stores, integrate_promotions,
    integrate_targets, calculate_metrics, transform_all
)
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


@pytest.fixture
def cleaned_data():
    raw = extract_all(DATA_DIR)
    cleaned_tx = clean_transactions(raw["transactions"])
    refs = clean_references(
        raw["products"], raw["stores"],
        raw["promotions"], raw["targets"]
    )
    return cleaned_tx, refs


@pytest.fixture
def with_promotions(cleaned_data):
    tx, refs = cleaned_data
    return integrate_promotions(tx, refs["promotions"])


class TestIntegrateProducts:
    def test_adds_product_name(self, cleaned_data):
        tx, refs = cleaned_data
        result = integrate_products(tx, refs["products"])
        assert "product_name" in result.columns
        assert "category" in result.columns


class TestIntegrateStores:
    def test_adds_store_info(self, cleaned_data):
        tx, refs = cleaned_data
        result = integrate_stores(tx, refs["stores"])
        assert "store_name" in result.columns
        assert "city" in result.columns
        assert "region" in result.columns


class TestIntegratePromotions:
    def test_adds_promotion_info(self, cleaned_data):
        tx, refs = cleaned_data
        result = integrate_promotions(tx, refs["promotions"])
        assert "discount_pct" in result.columns
        assert "campaign_name" in result.columns


class TestCalculateMetrics:
    def test_gross_sales(self, with_promotions):
        result = calculate_metrics(with_promotions)
        expected = result["quantity"] * result["unit_price"]
        assert result["gross_sales"].equals(expected)

    def test_net_sales(self, with_promotions):
        result = calculate_metrics(with_promotions)
        expected = result["gross_sales"] - result["discount_amount"]
        assert result["net_sales"].equals(expected)

    def test_month_column(self, with_promotions):
        result = calculate_metrics(with_promotions)
        assert "month" in result.columns
        assert "week" in result.columns
        assert "day_name" in result.columns


class TestTransformAll:
    def test_output_shape(self, cleaned_data):
        tx, refs = cleaned_data
        result = transform_all(tx, refs["products"], refs["stores"],
                               refs["promotions"], refs["targets"])
        assert len(result) > 0
        assert len(result.columns) > 10

    def test_has_all_derived_columns(self, cleaned_data):
        tx, refs = cleaned_data
        result = transform_all(tx, refs["products"], refs["stores"],
                               refs["promotions"], refs["targets"])
        expected = {"gross_sales", "discount_amount", "net_sales",
                    "month", "week", "day_name"}
        assert expected.issubset(set(result.columns))

"""
Tests for profile module.
"""
import pytest
import pandas as pd
from pathlib import Path
from src.profile import profile_dataframe, generate_profile_report, save_profile_report
from src.extract import extract_all

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "output"


@pytest.fixture
def raw_data():
    return extract_all(DATA_DIR)


class TestProfileDataframe:
    def test_returns_dict(self, raw_data):
        prof = profile_dataframe(raw_data["transactions"], "transactions")
        assert isinstance(prof, dict)

    def test_has_required_fields(self, raw_data):
        prof = profile_dataframe(raw_data["transactions"], "transactions")
        assert "rows" in prof
        assert "num_columns" in prof
        assert "columns" in prof
        assert "dtypes" in prof
        assert "nulls_per_column" in prof
        assert "total_nulls" in prof
        assert "duplicates" in prof

    def test_row_count(self, raw_data):
        prof = profile_dataframe(raw_data["transactions"], "transactions")
        assert prof["rows"] == len(raw_data["transactions"])

    def test_duplicate_ids(self, raw_data):
        prof = profile_dataframe(raw_data["transactions"], "transactions")
        assert "duplicate_sale_line_id" in prof
        assert prof["duplicate_sale_line_id"] >= 0

    def test_invalid_quantities(self, raw_data):
        prof = profile_dataframe(raw_data["transactions"], "transactions")
        assert "invalid_quantities" in prof
        assert "invalid_quantity_pct" in prof

    def test_invalid_prices(self, raw_data):
        prof = profile_dataframe(raw_data["transactions"], "transactions")
        assert "invalid_prices" in prof
        assert "invalid_price_pct" in prof

    def test_invalid_dates(self, raw_data):
        prof = profile_dataframe(raw_data["transactions"], "transactions")
        assert "invalid_dates" in prof
        assert "invalid_date_pct" in prof

    def test_distinct_values(self, raw_data):
        prof = profile_dataframe(raw_data["transactions"], "transactions")
        assert "distinct_values" in prof
        assert "store_id" in prof["distinct_values"]

    def test_dtypes_stringified(self, raw_data):
        prof = profile_dataframe(raw_data["transactions"], "transactions")
        for dtype_val in prof["dtypes"].values():
            assert isinstance(dtype_val, str)


class TestGenerateProfileReport:
    def test_returns_string(self, raw_data):
        profs = {}
        for name, df in raw_data.items():
            profs[name] = profile_dataframe(df, name)
        report = generate_profile_report(profs)
        assert isinstance(report, str)

    def test_contains_dataset_names(self, raw_data):
        profs = {}
        for name, df in raw_data.items():
            profs[name] = profile_dataframe(df, name)
        report = generate_profile_report(profs)
        assert "transactions" in report
        assert "products" in report


class TestSaveProfileReport:
    def test_creates_file(self, raw_data):
        profs = {}
        for name, df in raw_data.items():
            profs[name] = profile_dataframe(df, name)
        filepath = save_profile_report(profs, OUTPUT_DIR)
        assert filepath.exists()
        assert filepath.name == "profile_report.txt"

    def test_file_has_content(self, raw_data):
        profs = {}
        for name, df in raw_data.items():
            profs[name] = profile_dataframe(df, name)
        filepath = save_profile_report(profs, OUTPUT_DIR)
        content = filepath.read_text(encoding="utf-8")
        assert len(content) > 100

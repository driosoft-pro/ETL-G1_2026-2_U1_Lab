"""
Validate module - data quality validation.
"""
import pandas as pd


def validate_unique_ids(df: pd.DataFrame) -> bool:
    """Verify sale_line_id uniqueness."""
    return not df["sale_line_id"].duplicated().any()


def validate_foreign_keys(df: pd.DataFrame, reference_tables: dict) -> bool:
    """Verify all foreign keys exist in reference tables."""
    products = set(reference_tables["products"]["product_id"])
    stores = set(reference_tables["stores"]["store_id"])

    missing_products = set(df["product_id"]) - products
    missing_stores = set(df["store_id"]) - stores

    if missing_products:
        print(f"Invalid product_ids: {missing_products}")
        return False
    if missing_stores:
        print(f"Invalid store_ids: {missing_stores}")
        return False
    return True


def validate_positive_sales(df: pd.DataFrame) -> bool:
    """Verify all sales amounts are positive."""
    cols = ["quantity", "unit_price", "gross_sales", "net_sales"]
    for col in cols:
        if col in df.columns and (df[col] <= 0).any():
            print(f"Non-positive values found in {col}")
            return False
    return True


def validate_formulas(df: pd.DataFrame) -> bool:
    """Verify calculated fields (net_sales = gross_sales - discount_amount)."""
    expected = df["gross_sales"] - df["discount_amount"]
    if not df["net_sales"].equals(expected):
        print("Formula mismatch: net_sales != gross_sales - discount_amount")
        return False
    return True


def validate_all(df: pd.DataFrame, reference_tables: dict) -> dict:
    """Run all validations and return results."""
    errors = []

    if not validate_unique_ids(df):
        errors.append("Duplicate sale_line_id found")

    if not validate_foreign_keys(df, reference_tables):
        errors.append("Foreign key violations found")

    if not validate_positive_sales(df):
        errors.append("Non-positive sales values found")

    if not validate_formulas(df):
        errors.append("Formula validation failed")

    return {"passed": len(errors) == 0, "errors": errors}

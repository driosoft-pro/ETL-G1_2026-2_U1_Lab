"""
Transform module - data transformation and integration.
"""
import pandas as pd


def integrate_products(df: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    """Join transactions with product master."""
    raise NotImplementedError("Implement product integration")


def integrate_stores(df: pd.DataFrame, stores: pd.DataFrame) -> pd.DataFrame:
    """Join with store information."""
    raise NotImplementedError("Implement store integration")


def integrate_promotions(df: pd.DataFrame, promotions: pd.DataFrame) -> pd.DataFrame:
    """Apply promotions and calculate discounts."""
    raise NotImplementedError("Implement promotions integration")


def integrate_targets(df: pd.DataFrame, targets: pd.DataFrame) -> pd.DataFrame:
    """Join with monthly targets."""
    raise NotImplementedError("Implement targets integration")


def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate derived columns:
    - gross_sales
    - discount_amount
    - net_sales
    - month, week, day_name
    """
    raise NotImplementedError("Implement metric calculations")


def transform_all(transactions: pd.DataFrame, products: pd.DataFrame,
                  stores: pd.DataFrame, promotions: pd.DataFrame,
                  targets: pd.DataFrame) -> pd.DataFrame:
    """Run full transformation pipeline."""
    raise NotImplementedError("Implement full transformation")

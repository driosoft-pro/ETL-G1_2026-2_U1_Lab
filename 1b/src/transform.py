"""
Transform module - data transformation and integration.
"""
import pandas as pd


def integrate_products(df: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    """Join transactions with product master."""
    merged = df.merge(
        products[["product_id", "product_name", "category"]],
        on="product_id", how="left"
    )
    return merged


def integrate_stores(df: pd.DataFrame, stores: pd.DataFrame) -> pd.DataFrame:
    """Join with store information."""
    merged = df.merge(
        stores[["store_id", "store_name", "city", "region"]],
        on="store_id", how="left"
    )
    return merged


def integrate_promotions(df: pd.DataFrame, promotions: pd.DataFrame) -> pd.DataFrame:
    """Apply promotions and calculate discounts."""
    merged = df.merge(
        promotions[["promotion_code", "discount_pct", "campaign_name"]],
        on="promotion_code", how="left"
    )
    merged["discount_pct"] = merged["discount_pct"].fillna(0)
    merged["campaign_name"] = merged["campaign_name"].fillna("")
    return merged


def integrate_targets(df: pd.DataFrame, targets: pd.DataFrame) -> pd.DataFrame:
    """Join with monthly targets."""
    merged = df.merge(
        targets[["store_id", "month", "sales_target"]],
        on=["store_id", "month"], how="left"
    )
    merged["sales_target"] = merged["sales_target"].fillna(0)
    return merged


def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate derived columns:
    - gross_sales
    - discount_amount
    - net_sales
    - month, week, day_name
    """
    df = df.copy()
    df["gross_sales"] = df["quantity"] * df["unit_price"]
    df["discount_amount"] = df["gross_sales"] * df["discount_pct"]
    df["net_sales"] = df["gross_sales"] - df["discount_amount"]
    df["month"] = df["sale_date"].dt.to_period("M").astype(str)
    df["week"] = df["sale_date"].dt.isocalendar().week.astype(int)
    df["day_name"] = df["sale_date"].dt.day_name()
    return df


def transform_all(transactions: pd.DataFrame, products: pd.DataFrame,
                  stores: pd.DataFrame, promotions: pd.DataFrame,
                  targets: pd.DataFrame) -> pd.DataFrame:
    """Run full transformation pipeline."""
    df = integrate_products(transactions, products)
    df = integrate_stores(df, stores)
    df = integrate_promotions(df, promotions)
    df = calculate_metrics(df)
    df = integrate_targets(df, targets)
    return df

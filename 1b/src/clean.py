"""
Clean module - data cleaning based on profiling results.
"""
import pandas as pd


STRING_COLUMNS = [
    "sale_line_id", "sale_date", "store_id",
    "product_id", "promotion_code", "payment_method"
]


def _parse_dates(series: pd.Series) -> pd.Series:
    """Parse dates in multiple formats: YYYY-MM-DD, DD/MM/YYYY, MM-DD-YYYY."""
    result = pd.to_datetime(series, format="%Y-%m-%d", errors="coerce")
    mask = result.isna()
    if mask.any():
        result[mask] = pd.to_datetime(series[mask], format="%d/%m/%Y", errors="coerce")
    mask = result.isna()
    if mask.any():
        result[mask] = pd.to_datetime(series[mask], format="%m-%d-%Y", errors="coerce")
    mask = result.isna()
    if mask.any():
        result[mask] = pd.to_datetime(series[mask], dayfirst=True, errors="coerce")
    return result


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply cleaning rules derived from profiling:
    - Handle nulls
    - Fix data types
    - Remove duplicates
    - Correct invalid values
    """
    df = df.copy()

    df.columns = [c.strip().lower() for c in df.columns]

    for col in STRING_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    for col in ["store_id", "product_id", "payment_method"]:
        if col in df.columns:
            df[col] = df[col].str.upper()

    df["sale_date"] = _parse_dates(df["sale_date"])
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

    df = df.drop_duplicates(subset="sale_line_id", keep="first")

    df = df.dropna(subset=["sale_line_id", "sale_date", "store_id", "product_id"])
    df = df[df["quantity"] > 0]
    df = df[df["unit_price"] > 0]

    df["promotion_code"] = df["promotion_code"].fillna("")
    df["promotion_code"] = df["promotion_code"].replace("null", "")

    return df.reset_index(drop=True)


def clean_references(products: pd.DataFrame, stores: pd.DataFrame,
                     promotions: pd.DataFrame, targets: pd.DataFrame) -> dict:
    """Clean reference tables."""
    def _clean(df):
        df = df.copy()
        df.columns = [c.strip().lower() for c in df.columns]
        for col in df.select_dtypes(include=["object", "string"]).columns:
            df[col] = df[col].astype(str).str.strip()
        for col in ["store_id", "product_id"]:
            if col in df.columns:
                df[col] = df[col].str.upper()
        return df

    return {
        "products": _clean(products),
        "stores": _clean(stores),
        "promotions": _clean(promotions),
        "targets": _clean(targets),
    }

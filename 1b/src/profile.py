"""
Profile module - data profiling and quality assessment.
"""
import pandas as pd


def profile_dataframe(df: pd.DataFrame) -> dict:
    """
    Calculate profiling metrics:
    - rows, columns, types
    - nulls, duplicates
    - invalid dates, prices, quantities
    - unique values
    """
    profile = {
        "rows": len(df),
        "columns": list(df.columns),
        "dtypes": df.dtypes.to_dict(),
        "nulls": df.isnull().sum().to_dict(),
        "duplicates": int(df.duplicated().sum()),
    }

    if "sale_line_id" in df.columns:
        profile["duplicate_ids"] = int(df["sale_line_id"].duplicated().sum())

    if "quantity" in df.columns:
        qty = pd.to_numeric(df["quantity"], errors="coerce")
        profile["invalid_quantity"] = int((qty <= 0).sum())

    if "unit_price" in df.columns:
        price = pd.to_numeric(df["unit_price"], errors="coerce")
        profile["invalid_price"] = int((price <= 0).sum())

    if "sale_date" in df.columns:
        invalid_dates = 0
        for val in df["sale_date"].dropna():
            try:
                pd.to_datetime(val)
            except Exception:
                invalid_dates += 1
        profile["invalid_dates"] = invalid_dates

    categorical_cols = df.select_dtypes(include=["object"]).columns
    profile["unique_values"] = {
        col: int(df[col].nunique()) for col in categorical_cols
    }

    return profile


def generate_profile_report(profiles: dict) -> str:
    """Generate a human-readable profiling report."""
    lines = ["=== Data Profile Report ===\n"]
    for name, prof in profiles.items():
        lines.append(f"Dataset: {name}")
        lines.append(f"  Rows: {prof['rows']}")
        lines.append(f"  Columns: {len(prof['columns'])}")
        lines.append(f"  Duplicates: {prof['duplicates']}")
        if "duplicate_ids" in prof:
            lines.append(f"  Duplicate IDs: {prof['duplicate_ids']}")
        if "invalid_quantity" in prof:
            lines.append(f"  Invalid quantities: {prof['invalid_quantity']}")
        if "invalid_price" in prof:
            lines.append(f"  Invalid prices: {prof['invalid_price']}")
        if "invalid_dates" in prof:
            lines.append(f"  Invalid dates: {prof['invalid_dates']}")
        null_total = sum(prof["nulls"].values())
        lines.append(f"  Total nulls: {null_total}")
        lines.append("")
    return "\n".join(lines)

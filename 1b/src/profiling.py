"""
Profile module - data profiling and quality assessment.
"""
import pandas as pd
from pathlib import Path


def profile_dataframe(df: pd.DataFrame, name: str = "dataset") -> dict:
    """
    Calculate profiling metrics for a single DataFrame:
    - Row count, columns and data types
    - Missing values per column
    - Duplicate sale_line_id values
    - Invalid quantities, prices, dates
    - Distinct values for selected categorical fields
    """
    profile = {
        "name": name,
        "rows": len(df),
        "num_columns": len(df.columns),
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "nulls_per_column": {},
        "total_nulls": 0,
        "duplicates": int(df.duplicated().sum()),
    }

    # Missing values
    nulls = df.isnull().sum()
    profile["nulls_per_column"] = {col: int(v) for col, v in nulls.items() if v > 0}
    profile["total_nulls"] = int(nulls.sum())

    # Duplicate sale_line_id
    if "sale_line_id" in df.columns:
        dup_count = int(df["sale_line_id"].duplicated().sum())
        profile["duplicate_sale_line_id"] = dup_count
        if dup_count > 0:
            dup_ids = df[df["sale_line_id"].duplicated(keep=False)]["sale_line_id"].unique().tolist()
            profile["duplicate_ids_sample"] = dup_ids[:10]

    # Invalid quantities
    if "quantity" in df.columns:
        qty = pd.to_numeric(df["quantity"], errors="coerce")
        invalid_qty = int(((qty <= 0) | qty.isna()).sum())
        profile["invalid_quantities"] = invalid_qty
        profile["invalid_quantity_pct"] = round(invalid_qty / len(df) * 100, 2)

    # Invalid prices
    if "unit_price" in df.columns:
        price = pd.to_numeric(df["unit_price"], errors="coerce")
        invalid_price = int(((price <= 0) | price.isna()).sum())
        profile["invalid_prices"] = invalid_price
        profile["invalid_price_pct"] = round(invalid_price / len(df) * 100, 2)

    # Invalid dates
    if "sale_date" in df.columns:
        invalid_dates = 0
        for val in df["sale_date"].dropna():
            try:
                pd.to_datetime(val)
            except Exception:
                invalid_dates += 1
        profile["invalid_dates"] = invalid_dates
        profile["invalid_date_pct"] = round(invalid_dates / len(df) * 100, 2)

    # Distinct values for categorical fields
    categorical_cols = df.select_dtypes(include=["object", "string"]).columns
    profile["distinct_values"] = {}
    for col in categorical_cols:
        unique_vals = df[col].dropna().unique()
        profile["distinct_values"][col] = {
            "count": int(len(unique_vals)),
            "sample": [str(v) for v in unique_vals[:10]],
        }

    return profile


def generate_profile_report(profiles: dict) -> str:
    """Generate a human-readable profiling report for all datasets."""
    lines = []
    lines.append("=" * 60)
    lines.append("           DATA PROFILING REPORT")
    lines.append("=" * 60)

    for name, prof in profiles.items():
        lines.append("")
        lines.append("-" * 60)
        lines.append(f"  Dataset: {name}")
        lines.append("-" * 60)

        lines.append(f"  Rows:                   {prof['rows']}")
        lines.append(f"  Columns:                {prof['num_columns']}")
        lines.append(f"  Total nulls:            {prof['total_nulls']}")
        lines.append(f"  Duplicate rows:         {prof['duplicates']}")

        if "duplicate_sale_line_id" in prof:
            lines.append(f"  Duplicate sale_line_id: {prof['duplicate_sale_line_id']}")

        # Missing values detail
        if prof["nulls_per_column"]:
            lines.append("")
            lines.append("  Missing values per column:")
            for col, count in prof["nulls_per_column"].items():
                pct = round(count / prof["rows"] * 100, 2)
                lines.append(f"    {col:<25} {count:>6}  ({pct}%)")

        # Invalid data
        if "invalid_quantities" in prof:
            lines.append("")
            lines.append("  Invalid data:")
            lines.append(f"    Invalid quantities:   {prof['invalid_quantities']}  ({prof['invalid_quantity_pct']}%)")
            lines.append(f"    Invalid prices:       {prof['invalid_prices']}  ({prof['invalid_price_pct']}%)")
            if "invalid_dates" in prof:
                lines.append(f"    Invalid dates:        {prof['invalid_dates']}  ({prof['invalid_date_pct']}%)")

        # Distinct values
        if prof["distinct_values"]:
            lines.append("")
            lines.append("  Distinct values (categorical):")
            for col, info in prof["distinct_values"].items():
                lines.append(f"    {col:<25} {info['count']:>4} unique")
                if info["sample"]:
                    lines.append(f"      sample: {', '.join(info['sample'][:5])}")

        # Data types
        lines.append("")
        lines.append("  Data types:")
        for col, dtype in prof["dtypes"].items():
            lines.append(f"    {col:<25} {dtype}")

    lines.append("")
    lines.append("=" * 60)
    lines.append("  END OF REPORT")
    lines.append("=" * 60)

    return "\n".join(lines)


def save_profile_report(profiles: dict, output_dir: Path) -> Path:
    """Save profiling report to file and return the path."""
    output_dir.mkdir(parents=True, exist_ok=True)
    report = generate_profile_report(profiles)
    filepath = output_dir / "profile_report.txt"
    filepath.write_text(report, encoding="utf-8")
    return filepath

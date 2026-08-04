"""
Clean module - data cleaning based on profiling results.
"""
import pandas as pd


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply cleaning rules derived from profiling:
    - Handle nulls
    - Fix data types
    - Remove duplicates
    - Correct invalid values
    """
    raise NotImplementedError("Implement cleaning rules")


def clean_references(products: pd.DataFrame, stores: pd.DataFrame,
                     promotions: pd.DataFrame, targets: pd.DataFrame) -> dict:
    """Clean reference tables."""
    raise NotImplementedError("Implement reference cleaning")

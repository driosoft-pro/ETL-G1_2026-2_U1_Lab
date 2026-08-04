"""
Extract module - reads data from CSV, JSON, and XML sources.
"""
import pandas as pd
import json
import xml.etree.ElementTree as ET
from pathlib import Path


def extract_csv(filepath: Path) -> pd.DataFrame:
    """Extract data from CSV file."""
    raise NotImplementedError("Implement CSV extraction")


def extract_json(filepath: Path) -> pd.DataFrame:
    """Extract data from JSON file."""
    raise NotImplementedError("Implement JSON extraction")


def extract_xml(filepath: Path) -> pd.DataFrame:
    """Extract data from XML file."""
    raise NotImplementedError("Implement XML extraction")


def extract_all(data_dir: Path) -> dict[str, pd.DataFrame]:
    """Extract all transaction sources and return unified schema DataFrames."""
    raise NotImplementedError("Implement full extraction pipeline")

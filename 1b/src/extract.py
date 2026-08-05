"""
Extract module - reads data from CSV, JSON, and XML sources.
"""
import pandas as pd
import json
import xml.etree.ElementTree as ET
from pathlib import Path


TRANSACTION_COLUMNS = [
    "sale_line_id", "sale_date", "store_id", "product_id",
    "quantity", "unit_price", "promotion_code", "payment_method"
]


def extract_csv(filepath: Path) -> pd.DataFrame:
    """Extract data from CSV file."""
    return pd.read_csv(filepath)


def extract_json(filepath: Path) -> pd.DataFrame:
    """Extract data from JSON file and standardize column names."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    column_map = {
        "id_linea": "sale_line_id",
        "fecha": "sale_date",
        "sucursal": "store_id",
        "codigo_producto": "product_id",
        "unidades": "quantity",
        "precio": "unit_price",
        "promocion": "promotion_code",
        "medio_pago": "payment_method",
    }
    df = df.rename(columns=column_map)
    return df[TRANSACTION_COLUMNS]


def extract_xml(filepath: Path) -> pd.DataFrame:
    """Extract data from XML file and standardize column names."""
    tree = ET.parse(filepath)
    root = tree.getroot()

    rows = []
    for sale in root.findall("sale"):
        row = {
            "sale_line_id": sale.findtext("line_id"),
            "sale_date": sale.findtext("date"),
            "store_id": sale.findtext("branch_code"),
            "product_id": sale.findtext("sku"),
            "quantity": sale.findtext("units"),
            "unit_price": sale.findtext("unit_value"),
            "promotion_code": sale.findtext("promo_code"),
            "payment_method": sale.findtext("payment"),
        }
        rows.append(row)

    df = pd.DataFrame(rows, columns=TRANSACTION_COLUMNS)
    return df


def extract_all(data_dir: Path) -> dict[str, pd.DataFrame]:
    """Extract all transaction sources and return unified schema DataFrames."""
    result = {}

    transactions = pd.concat([
        extract_csv(data_dir / "sales_cali.csv"),
        extract_json(data_dir / "sales_bogota.json"),
        extract_xml(data_dir / "sales_medellin.xml"),
    ], ignore_index=True)

    result["transactions"] = transactions
    result["products"] = extract_csv(data_dir / "products.csv")
    result["stores"] = extract_csv(data_dir / "stores.csv")
    result["promotions"] = extract_csv(data_dir / "promotions.csv")
    result["targets"] = extract_csv(data_dir / "monthly_targets.csv")

    return result

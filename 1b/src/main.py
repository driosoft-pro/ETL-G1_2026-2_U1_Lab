"""
Main module - ETL pipeline orchestration.
"""
import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/etl.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SRC_DIR = BASE_DIR / "src"

sys.path.insert(0, str(SRC_DIR))

from extract import extract_all
from profile import profile_dataframe
from clean import clean_transactions, clean_references
from transform import transform_all
from validate import validate_all
from load import load_to_csv, load_to_sqlite, create_tables
from queries import run_queries


def run_pipeline():
    """Execute the full ETL pipeline."""
    logger.info("=== Starting ETL Pipeline ===")

    try:
        logger.info("Phase 0: Initialize SQLite database")
        db_path = DATA_DIR / "retail_analytics.db"
        create_tables(db_path)

        logger.info("Phase 1: Extract")
        raw_data = extract_all(DATA_DIR / "raw")

        logger.info("Phase 2: Profile")
        for name, df in raw_data.items():
            profile = profile_dataframe(df)
            logger.info(f"Profile for {name}: {profile}")

        logger.info("Phase 3: Clean")
        cleaned_transactions = clean_transactions(raw_data["transactions"])
        cleaned_refs = clean_references(
            raw_data["products"], raw_data["stores"],
            raw_data["promotions"], raw_data["targets"]
        )

        logger.info("Phase 4: Transform")
        integrated = transform_all(
            cleaned_transactions, cleaned_refs["products"],
            cleaned_refs["stores"], cleaned_refs["promotions"],
            cleaned_refs["targets"]
        )

        logger.info("Phase 5: Validate")
        validation = validate_all(integrated, cleaned_refs)
        if not validation["passed"]:
            logger.error(f"Validation failed: {validation['errors']}")
            raise ValueError("Data validation failed")

        logger.info("Phase 6: Load")
        load_to_csv(integrated, DATA_DIR / "processed" / "sales_analytics.csv")
        load_to_sqlite(integrated, "sales_analytics", db_path)

        logger.info("Phase 7: Queries")
        results = run_queries(db_path)
        for name, df in results.items():
            logger.info(f"Query '{name}': {len(df)} rows returned")

        logger.info("=== ETL Pipeline completed successfully ===")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise


if __name__ == "__main__":
    run_pipeline()

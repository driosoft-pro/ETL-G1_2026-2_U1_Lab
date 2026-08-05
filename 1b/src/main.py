"""
Main module - ETL pipeline orchestration with interactive menu.
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

STEPS = [
    ("1", "Initialize database", "Create SQLite database and tables"),
    ("2", "Extract data", "Read CSV, JSON, and XML source files"),
    ("3", "Profile data", "Analyze data quality and statistics"),
    ("4", "Clean data", "Standardize, deduplicate, and validate records"),
    ("5", "Transform data", "Join tables and compute derived columns"),
    ("6", "Validate data", "Verify integrity rules and constraints"),
    ("7", "Load data", "Export to CSV and load into SQLite"),
    ("8", "Run queries", "Execute analytical queries for business KPIs"),
    ("9", "Run full pipeline", "Execute all steps sequentially with progress"),
]


def confirm(step_name: str) -> bool:
    resp = input(f"\nRun '{step_name}'? [y/N]: ").strip().lower()
    return resp in ("y", "yes")


def show_menu():
    print("\n" + "=" * 50)
    print("       ETL PIPELINE - RETAIL ANALYTICS")
    print("=" * 50)
    for num, name, desc in STEPS:
        print(f"  [{num}] {name:<25} - {desc}")
    print("  [0] Exit")
    print("=" * 50)


def run_pipeline():
    """Execute the full ETL pipeline step by step with progress."""
    total = 8
    logger.info("=== Starting ETL Pipeline ===")
    print("\n--- Running Full Pipeline ---\n")

    try:
        print(f"[1/{total}] Initializing database...")
        db_path = DATA_DIR / "retail_analytics.db"
        create_tables(db_path)
        print(f"[1/{total}] Database initialized.\n")

        print(f"[2/{total}] Extracting data...")
        raw_data = extract_all(DATA_DIR / "raw")
        print(f"[2/{total}] Extracted {len(raw_data)} datasets.\n")

        print(f"[3/{total}] Profiling data...")
        for name, df in raw_data.items():
            profile = profile_dataframe(df)
            logger.info(f"Profile for {name}: {profile}")
        print(f"[3/{total}] Profiling done.\n")

        print(f"[4/{total}] Cleaning data...")
        cleaned_transactions = clean_transactions(raw_data["transactions"])
        cleaned_refs = clean_references(
            raw_data["products"], raw_data["stores"],
            raw_data["promotions"], raw_data["targets"]
        )
        print(f"[4/{total}] Data cleaned.\n")

        print(f"[5/{total}] Transforming data...")
        integrated = transform_all(
            cleaned_transactions, cleaned_refs["products"],
            cleaned_refs["stores"], cleaned_refs["promotions"],
            cleaned_refs["targets"]
        )
        print(f"[5/{total}] Data transformed.\n")

        print(f"[6/{total}] Validating data...")
        validation = validate_all(integrated, cleaned_refs)
        if not validation["passed"]:
            logger.error(f"Validation failed: {validation['errors']}")
            raise ValueError("Data validation failed")
        print(f"[6/{total}] Validation passed.\n")

        print(f"[7/{total}] Loading data...")
        load_to_csv(integrated, DATA_DIR / "processed" / "sales_analytics.csv")
        load_to_sqlite(integrated, "sales_analytics", db_path)
        print(f"[7/{total}] Data loaded.\n")

        print(f"[8/{total}] Running analytical queries...")
        results = run_queries(db_path)
        for name, df in results.items():
            logger.info(f"Query '{name}': {len(df)} rows returned")
        print(f"[8/{total}] Queries done.\n")

        print("=== ETL Pipeline completed successfully ===\n")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        print(f"\nPipeline failed: {e}")
        raise


def step_initialize_db():
    logger.info("Phase 0: Initialize SQLite database")
    create_tables(DATA_DIR / "retail_analytics.db")
    logger.info("Database initialized.")


def step_extract():
    logger.info("Phase 1: Extract")
    raw_data = extract_all(DATA_DIR / "raw")
    logger.info(f"Extracted {len(raw_data)} datasets.")
    return raw_data


def step_profile(raw_data):
    logger.info("Phase 2: Profile")
    for name, df in raw_data.items():
        profile = profile_dataframe(df)
        logger.info(f"Profile for {name}: {profile}")


def step_clean(raw_data):
    logger.info("Phase 3: Clean")
    cleaned_transactions = clean_transactions(raw_data["transactions"])
    cleaned_refs = clean_references(
        raw_data["products"], raw_data["stores"],
        raw_data["promotions"], raw_data["targets"]
    )
    logger.info("Data cleaned.")
    return cleaned_transactions, cleaned_refs


def step_transform(cleaned_transactions, cleaned_refs):
    logger.info("Phase 4: Transform")
    integrated = transform_all(
        cleaned_transactions, cleaned_refs["products"],
        cleaned_refs["stores"], cleaned_refs["promotions"],
        cleaned_refs["targets"]
    )
    logger.info("Data transformed and integrated.")
    return integrated


def step_validate(integrated, cleaned_refs):
    logger.info("Phase 5: Validate")
    validation = validate_all(integrated, cleaned_refs)
    if not validation["passed"]:
        logger.error(f"Validation failed: {validation['errors']}")
        raise ValueError("Data validation failed")
    logger.info("Validation passed.")
    return True


def step_load(integrated):
    logger.info("Phase 6: Load")
    db_path = DATA_DIR / "retail_analytics.db"
    load_to_csv(integrated, DATA_DIR / "processed" / "sales_analytics.csv")
    load_to_sqlite(integrated, "sales_analytics", db_path)
    logger.info("Data loaded to CSV and SQLite.")


def step_queries():
    logger.info("Phase 7: Queries")
    db_path = DATA_DIR / "retail_analytics.db"
    results = run_queries(db_path)
    for name, df in results.items():
        logger.info(f"Query '{name}': {len(df)} rows returned")


if __name__ == "__main__":
    show_menu()

    while True:
        choice = input("\nSelect an option: ").strip()

        if choice == "0":
            print("Exiting.")
            break

        if choice == "9":
            if confirm("Run full pipeline"):
                run_pipeline()
            continue

        selected = next((s for s in STEPS if s[0] == choice), None)
        if not selected:
            print("Invalid option. Try again.")
            continue

        if not confirm(selected[1]):
            continue

        try:
            if choice == "1":
                step_initialize_db()
            elif choice == "2":
                raw_data = step_extract()
            elif choice == "3":
                raw_data = extract_all(DATA_DIR / "raw")
                step_profile(raw_data)
            elif choice == "4":
                raw_data = extract_all(DATA_DIR / "raw")
                cleaned_transactions, cleaned_refs = step_clean(raw_data)
            elif choice == "5":
                raw_data = extract_all(DATA_DIR / "raw")
                cleaned_transactions, cleaned_refs = step_clean(raw_data)
                integrated = step_transform(cleaned_transactions, cleaned_refs)
            elif choice == "6":
                raw_data = extract_all(DATA_DIR / "raw")
                cleaned_transactions, cleaned_refs = step_clean(raw_data)
                integrated = step_transform(cleaned_transactions, cleaned_refs)
                step_validate(integrated, cleaned_refs)
            elif choice == "7":
                raw_data = extract_all(DATA_DIR / "raw")
                cleaned_transactions, cleaned_refs = step_clean(raw_data)
                integrated = step_transform(cleaned_transactions, cleaned_refs)
                step_load(integrated)
            elif choice == "8":
                step_queries()
        except Exception as e:
            logger.error(f"Step failed: {e}")
            print(f"Error: {e}")

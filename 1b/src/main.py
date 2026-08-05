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


def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")


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


def run_step(label: str, func, *args, **kwargs):
    """Execute a step and print OK or ERROR."""
    try:
        result = func(*args, **kwargs)
        print(f"  {label} [ OK ]")
        return result
    except Exception as e:
        print(f"  {label} [ERROR] {e}")
        logger.error(f"{label} failed: {e}")
        raise


def run_pipeline():
    """Execute the full ETL pipeline step by step with progress."""
    total = 8
    print("\n--- Running Full Pipeline ---\n")

    try:
        db_path = DATA_DIR / "retail_analytics.db"
        run_step(f"[1/{total}] Initialize DB", create_tables, db_path)
        raw_data = run_step(f"[2/{total}] Extract", extract_all, DATA_DIR / "raw")
        run_step(f"[3/{total}] Profile", _run_profiles, raw_data)
        cleaned = run_step(f"[4/{total}] Clean", _run_clean, raw_data)
        integrated = run_step(f"[5/{total}] Transform", _run_transform, cleaned, raw_data)
        run_step(f"[6/{total}] Validate", _run_validate, integrated, cleaned)
        run_step(f"[7/{total}] Load", _run_load, integrated, db_path)
        run_step(f"[8/{total}] Queries", run_queries, db_path)

        print("\n=== ETL Pipeline completed successfully ===\n")

    except Exception as e:
        print(f"\n=== Pipeline aborted: {e} ===\n")
        raise


def _run_profiles(raw_data):
    for name, df in raw_data.items():
        profile_dataframe(df)


def _run_clean(raw_data):
    cleaned_transactions = clean_transactions(raw_data["transactions"])
    cleaned_refs = clean_references(
        raw_data["products"], raw_data["stores"],
        raw_data["promotions"], raw_data["targets"]
    )
    return cleaned_transactions, cleaned_refs


def _run_transform(cleaned, raw_data):
    cleaned_transactions, cleaned_refs = cleaned
    return transform_all(
        cleaned_transactions, cleaned_refs["products"],
        cleaned_refs["stores"], cleaned_refs["promotions"],
        cleaned_refs["targets"]
    )


def _run_validate(integrated, cleaned):
    _, cleaned_refs = cleaned
    validation = validate_all(integrated, cleaned_refs)
    if not validation["passed"]:
        raise ValueError(f"Validation errors: {validation['errors']}")


def _run_load(integrated, db_path):
    load_to_csv(integrated, DATA_DIR / "processed" / "sales_analytics.csv")
    load_to_sqlite(integrated, "sales_analytics", db_path)


if __name__ == "__main__":
    while True:
        clear_screen()
        show_menu()

        choice = input("\nSelect an option: ").strip()

        if choice == "0":
            print("Exiting.")
            break

        if choice == "9":
            if confirm("Run full pipeline"):
                run_pipeline()
            input("\nPress Enter to continue...")
            continue

        selected = next((s for s in STEPS if s[0] == choice), None)
        if not selected:
            print("Invalid option.")
            input("\nPress Enter to continue...")
            continue

        if not confirm(selected[1]):
            input("\nPress Enter to continue...")
            continue

        try:
            if choice == "1":
                run_step("[1] Initialize DB", create_tables, DATA_DIR / "retail_analytics.db")
            elif choice == "2":
                run_step("[2] Extract", extract_all, DATA_DIR / "raw")
            elif choice == "3":
                raw_data = run_step("[3.1] Extract", extract_all, DATA_DIR / "raw")
                run_step("[3.2] Profile", _run_profiles, raw_data)
            elif choice == "4":
                raw_data = run_step("[4.1] Extract", extract_all, DATA_DIR / "raw")
                run_step("[4.2] Clean", _run_clean, raw_data)
            elif choice == "5":
                raw_data = run_step("[5.1] Extract", extract_all, DATA_DIR / "raw")
                cleaned = run_step("[5.2] Clean", _run_clean, raw_data)
                run_step("[5.3] Transform", _run_transform, cleaned, raw_data)
            elif choice == "6":
                raw_data = run_step("[6.1] Extract", extract_all, DATA_DIR / "raw")
                cleaned = run_step("[6.2] Clean", _run_clean, raw_data)
                integrated = run_step("[6.3] Transform", _run_transform, cleaned, raw_data)
                run_step("[6.4] Validate", _run_validate, integrated, cleaned)
            elif choice == "7":
                raw_data = run_step("[7.1] Extract", extract_all, DATA_DIR / "raw")
                cleaned = run_step("[7.2] Clean", _run_clean, raw_data)
                integrated = run_step("[7.3] Transform", _run_transform, cleaned, raw_data)
                run_step("[7.4] Load", _run_load, integrated, DATA_DIR / "retail_analytics.db")
            elif choice == "8":
                run_step("[8] Queries", run_queries, DATA_DIR / "retail_analytics.db")
        except Exception:
            pass

        input("\nPress Enter to continue...")

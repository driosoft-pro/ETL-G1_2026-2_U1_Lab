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

from extract import extract_all, extract_csv
from profile import profile_dataframe, save_profile_report
from clean import clean_transactions, clean_references
from transform import transform_all
from validate import validate_all
from load import load_to_csv, load_to_sqlite, load_references_to_sqlite, create_tables, create_vanilla_database
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
    ("10", "Create vanilla DB", "Export raw data to vanilla_analytics.db (no treatment)"),
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


OUTPUT_DIR = DATA_DIR / "output"


def run_pipeline():
    """Execute the full ETL pipeline step by step with progress."""
    total = 9
    print("\n--- Running Full Pipeline ---\n")

    try:
        db_path = DATA_DIR / "retail_analytics.db"

        # Step 1: Initialize DB
        print(f"\n[1/{total}] Initialize database")
        create_tables(db_path)
        print(f"  Database created at {db_path}")
        print(f"  [1/{total}] Initialize DB [ OK ]")

        # Step 2: Extract
        print(f"\n[2/{total}] Extracting data from source files...")
        raw_data = extract_all(DATA_DIR / "raw")
        csv_df = extract_csv(DATA_DIR / "raw" / "sales_cali.csv")
        print(f"  CSV (Cali): {len(csv_df)} rows")
        print(f"  JSON (Bogotá): {len(raw_data['transactions']) - len(csv_df)} rows")
        print(f"  XML (Medellín): {len(raw_data['transactions']) - len(csv_df)} rows")
        print(f"  Total transactions: {len(raw_data['transactions'])} rows")
        print(f"  Reference tables: products({len(raw_data['products'])}), stores({len(raw_data['stores'])}), promotions({len(raw_data['promotions'])}), targets({len(raw_data['targets'])})")
        print(f"  [2/{total}] Extract [ OK ]")

        # Step 3: Profile
        print(f"\n[3/{total}] Profiling data quality...")
        _run_profiles(raw_data)
        print(f"  [3/{total}] Profile [ OK ]")

        # Step 4: Clean
        print(f"\n[4/{total}] Cleaning transactions...")
        cleaned = _run_clean(raw_data)
        cleaned_transactions, cleaned_refs = cleaned
        removed = len(raw_data["transactions"]) - len(cleaned_transactions)
        print(f"  Removed {removed} rows (duplicates, invalids, nulls)")
        print(f"  Remaining: {len(cleaned_transactions)} transactions")
        print(f"  [4/{total}] Clean [ OK ]")

        # Step 5: Transform
        print(f"\n[5/{total}] Transforming data...")
        integrated = _run_transform(cleaned, raw_data)
        print(f"  Joined products, stores, promotions, targets")
        print(f"  Calculated: gross_sales, discount_amount, net_sales")
        print(f"  Added: month, week, day_name")
        print(f"  Total rows: {len(integrated)}")
        print(f"  [5/{total}] Transform [ OK ]")

        # Step 6: Validate
        print(f"\n[6/{total}] Validating data integrity...")
        validation = validate_all(integrated, cleaned_refs)
        if validation["passed"]:
            print(f"  All validations passed:")
            print(f"    - Unique sale_line_id")
            print(f"    - Foreign key integrity")
            print(f"    - Positive sales values")
            print(f"    - Formula correctness")
        else:
            raise ValueError(f"Validation errors: {validation['errors']}")
        print(f"  [6/{total}] Validate [ OK ]")

        # Step 7: Load
        print(f"\n[7/{total}] Loading data...")
        load_to_csv(integrated, DATA_DIR / "processed" / "sales_analytics.csv")
        print(f"  CSV: data/processed/sales_analytics.csv")
        load_to_sqlite(integrated, "sales_analytics", db_path)
        print(f"  SQLite: sales_analytics table ({len(integrated)} rows)")
        _, cleaned_refs = cleaned
        load_references_to_sqlite(cleaned_refs, db_path)
        print(f"  [7/{total}] Load [ OK ]")

        # Step 8: Queries
        print(f"\n[8/{total}] Running analytical queries...")
        results = run_queries(db_path)
        for name in results:
            print(f"  - {name}: {len(results[name])} rows")
        print(f"  [8/{total}] Queries [ OK ]")

        # Step 9: Save outputs
        print(f"\n[9/{total}] Saving outputs...")
        _save_outputs(db_path)
        files = list(OUTPUT_DIR.glob("*.csv"))
        print(f"  Saved {len(files)} CSV files to {OUTPUT_DIR}")
        report = OUTPUT_DIR / "profile_report.txt"
        if report.exists():
            print(f"  Profile report: profile_report.txt")
        print(f"  [9/{total}] Save outputs [ OK ]")

        print("\n" + "=" * 50)
        print("  Pipeline completed successfully!")
        print("=" * 50 + "\n")

    except Exception as e:
        print(f"\n=== Pipeline aborted: {e} ===\n")
        raise


def _save_outputs(db_path):
    """Clear and save query results and reports to data/output/."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for f in OUTPUT_DIR.glob("*.csv"):
        f.unlink()
    results = run_queries(db_path)
    for name, df in results.items():
        df.to_csv(OUTPUT_DIR / f"{name}.csv", index=False)
    logger.info(f"Outputs saved to {OUTPUT_DIR}")


def _run_profiles(raw_data):
    """Profile all datasets, save report, and print it."""
    profiles = {}
    for name, df in raw_data.items():
        profiles[name] = profile_dataframe(df, name)
        print(f"  {name}: {len(df)} rows, {len(df.columns)} columns")
    report = save_profile_report(profiles, OUTPUT_DIR)
    report_text = report.read_text(encoding="utf-8")
    print(f"\n{report_text}\n")
    logger.info(f"Profile report saved to {report}")
    return profiles


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


def _run_load(integrated, cleaned, db_path):
    load_to_csv(integrated, DATA_DIR / "processed" / "sales_analytics.csv")
    load_to_sqlite(integrated, "sales_analytics", db_path)
    _, cleaned_refs = cleaned
    load_references_to_sqlite(cleaned_refs, db_path)


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
            clear_screen()
            continue

        if choice == "10":
            if confirm("Create vanilla_analytics.db (raw data, no treatment)"):
                print("\n--- Creating Vanilla Database ---\n")
                raw_data = extract_all(DATA_DIR / "raw")
                vanilla_path = DATA_DIR / "vanilla_analytics.db"
                create_vanilla_database(raw_data, vanilla_path)
                print(f"\n  Vanilla database created at {vanilla_path}")
                print(f"  Tables: sales_raw, products, stores, promotions, monthly_targets")
                print(f"  All data is raw (no cleaning, no type conversion)")
            input("\nPress Enter to continue...")
            clear_screen()
            continue

        selected = next((s for s in STEPS if s[0] == choice), None)
        if not selected:
            print("Invalid option.")
            input("\nPress Enter to continue...")
            clear_screen()
            continue

        if not confirm(selected[1]):
            input("\nPress Enter to continue...")
            clear_screen()
            continue

        try:
            if choice == "1":
                create_tables(DATA_DIR / "retail_analytics.db")
                print(f"  Database created at {DATA_DIR / 'retail_analytics.db'}")
            elif choice == "2":
                raw_data = extract_all(DATA_DIR / "raw")
                n = len(raw_data["transactions"])
                print(f"  CSV: {n} rows from sales_cali.csv")
                print(f"  JSON: rows from sales_bogota.json")
                print(f"  XML: rows from sales_medellin.xml")
                print(f"  Reference tables: products({len(raw_data['products'])}), stores({len(raw_data['stores'])}), promotions({len(raw_data['promotions'])}), targets({len(raw_data['targets'])})")
            elif choice == "3":
                raw_data = extract_all(DATA_DIR / "raw")
                _run_profiles(raw_data)
            elif choice == "4":
                raw_data = extract_all(DATA_DIR / "raw")
                n_before = len(raw_data["transactions"])
                cleaned = _run_clean(raw_data)
                n_after = len(cleaned[0])
                print(f"  Removed {n_before - n_after} rows (duplicates, invalids, nulls)")
                print(f"  Remaining: {n_after} transactions")
            elif choice == "5":
                raw_data = extract_all(DATA_DIR / "raw")
                cleaned = _run_clean(raw_data)
                integrated = _run_transform(cleaned, raw_data)
                print(f"  Joined products, stores, promotions, targets")
                print(f"  Calculated: gross_sales, discount_amount, net_sales")
                print(f"  Added: month, week, day_name")
                print(f"  Total rows: {len(integrated)}")
            elif choice == "6":
                raw_data = extract_all(DATA_DIR / "raw")
                cleaned = _run_clean(raw_data)
                integrated = _run_transform(cleaned, raw_data)
                validation = validate_all(integrated, cleaned[1])
                if validation["passed"]:
                    print(f"  All validations passed:")
                    print(f"    - Unique sale_line_id")
                    print(f"    - Foreign key integrity")
                    print(f"    - Positive sales values")
                    print(f"    - Formula correctness")
                else:
                    raise ValueError(f"Validation errors: {validation['errors']}")
            elif choice == "7":
                raw_data = extract_all(DATA_DIR / "raw")
                cleaned = _run_clean(raw_data)
                integrated = _run_transform(cleaned, raw_data)
                load_to_csv(integrated, DATA_DIR / "processed" / "sales_analytics.csv")
                print(f"  CSV: data/processed/sales_analytics.csv")
                load_to_sqlite(integrated, "sales_analytics", DATA_DIR / "retail_analytics.db")
                print(f"  SQLite: sales_analytics table ({len(integrated)} rows)")
                _, cleaned_refs = cleaned
                load_references_to_sqlite(cleaned_refs, DATA_DIR / "retail_analytics.db")
            elif choice == "8":
                results = run_queries(DATA_DIR / "retail_analytics.db")
                for name in results:
                    print(f"  - {name}: {len(results[name])} rows")
                _save_outputs(DATA_DIR / "retail_analytics.db")
                files = list(OUTPUT_DIR.glob("*.csv"))
                print(f"  Saved {len(files)} CSV files to {OUTPUT_DIR}")
        except Exception:
            pass

        input("\nPress Enter to continue...")
        clear_screen()

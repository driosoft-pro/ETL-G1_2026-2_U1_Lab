"""
Queries module - SQL queries for business requirements using SQLite.
"""
import os
import sqlite3
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DB_PATH = Path(os.getenv("DB_PATH", "data/retail_analytics.db"))


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """Get a SQLite connection."""
    return sqlite3.connect(str(db_path))


def run_queries(db_path: Path = DB_PATH) -> dict:
    """
    Execute SQL queries that answer the business requirements
    defined in Lab 1A.
    """
    conn = get_connection(db_path)
    results = {}
    try:
        results["top_products"] = query_top_products(conn)
        results["monthly_performance"] = query_monthly_performance(conn)
        results["regional_analysis"] = query_regional_analysis(conn)
        results["sales_by_region"] = query_sales_by_region(conn)
        results["sales_by_category"] = query_sales_by_category(conn)
        results["goal_compliance"] = query_goal_compliance(conn)
    finally:
        conn.close()
    return results


def query_top_products(conn) -> pd.DataFrame:
    """Query top-selling products by net sales."""
    query = """
        SELECT product_id, product_name, category,
               SUM(net_sales) AS total_net_sales,
               SUM(quantity) AS total_units
        FROM sales_analytics
        GROUP BY product_id, product_name, category
        ORDER BY total_net_sales DESC
        LIMIT 10
    """
    return pd.read_sql_query(query, conn)


def query_monthly_performance(conn) -> pd.DataFrame:
    """Query monthly performance vs targets."""
    query = """
        SELECT store_id, store_name,
               month,
               sales_target,
               SUM(net_sales) AS actual_sales,
               ROUND(SUM(net_sales) / sales_target * 100, 2) AS achievement_pct
        FROM sales_analytics
        GROUP BY store_id, store_name, month, sales_target
        ORDER BY month, store_id
    """
    return pd.read_sql_query(query, conn)


def query_regional_analysis(conn) -> pd.DataFrame:
    """Query regional sales analysis."""
    query = """
        SELECT region, city, store_id, store_name,
               SUM(net_sales) AS total_net_sales,
               SUM(quantity) AS total_units,
               COUNT(DISTINCT sale_date) AS active_days
        FROM sales_analytics
        GROUP BY region, city, store_id, store_name
        ORDER BY region, total_net_sales DESC
    """
    return pd.read_sql_query(query, conn)


def query_sales_by_region(conn) -> pd.DataFrame:
    """Query total sales by region."""
    query = """
        SELECT region,
               SUM(net_sales) AS total_net_sales,
               SUM(quantity) AS total_units,
               COUNT(DISTINCT store_id) AS num_stores
        FROM sales_analytics
        GROUP BY region
        ORDER BY total_net_sales DESC
    """
    return pd.read_sql_query(query, conn)


def query_sales_by_category(conn) -> pd.DataFrame:
    """Query total sales by product category."""
    query = """
        SELECT category,
               SUM(net_sales) AS total_net_sales,
               SUM(quantity) AS total_units,
               COUNT(DISTINCT product_id) AS num_products
        FROM sales_analytics
        GROUP BY category
        ORDER BY total_net_sales DESC
    """
    return pd.read_sql_query(query, conn)


def query_goal_compliance(conn) -> pd.DataFrame:
    """Query goal compliance by store and month."""
    query = """
        SELECT store_id, store_name,
               month,
               sales_target,
               SUM(net_sales) AS actual_sales,
               ROUND(SUM(net_sales) / sales_target * 100, 2) AS achievement_pct,
               CASE
                   WHEN SUM(net_sales) >= sales_target THEN 'Met'
                   ELSE 'Not Met'
               END AS status
        FROM sales_analytics
        GROUP BY store_id, store_name, month, sales_target
        ORDER BY month, store_id
    """
    return pd.read_sql_query(query, conn)

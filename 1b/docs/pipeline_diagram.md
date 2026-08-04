# Pipeline Block Diagram

## ETL Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        BUSINESS REQUIREMENTS (Lab 1A)                       │
│  • Visualize total sales by period    • Measure goal compliance             │
│  • Analyze sales by region            • Analyze promotion impact            │
│  • Compare store performance          • Analyze product/category performance│
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA SOURCES                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ sales_cali   │  │ sales_bogota │  │sales_medellin│  │  Reference   │   │
│  │    .csv      │  │    .json     │  │    .xml      │  │    Tables    │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                               EXTRACT                                        │
│  • Read CSV files (Cali, products, stores, promotions, targets)            │
│  • Read JSON file (Bogota)                                                  │
│  • Read XML file (Medellin)                                                 │
│  • Convert to pandas DataFrames with common schema                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                               PROFILE                                        │
│  • Row count, columns and data types                                        │
│  • Missing values                                                           │
│  • Duplicate sale_line_id values                                            │
│  • Invalid quantities, prices, dates                                        │
│  • Distinct values for categorical fields                                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          CLEAN / HARMONIZE                                   │
│  • Standardize column names and ID values                                   │
│  • Trim whitespace and standardize text casing                              │
│  • Parse date formats into one date type                                    │
│  • Convert quantity and unit_price to numeric                               │
│  • Remove duplicated sale_line_id records                                   │
│  • Reject invalid records (dates, quantity <= 0, unit_price <= 0)          │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        TRANSFORM / INTEGRATE                                │
│  • Join with products: product_name, category                               │
│  • Join with stores: store_name, city, region                               │
│  • Join with promotions: discount_pct, campaign_name                        │
│  • Join with targets: sales_target                                          │
│  • Calculate: gross_sales, discount_amount, net_sales                       │
│  • Extract: month, week, day_name from sale_date                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              VALIDATE                                        │
│  • sale_line_id is unique                                                   │
│  • Required identifiers and dates are not null                              │
│  • quantity, unit_price, gross_sales, net_sales are positive                │
│  • Every product matches the product master                                 │
│  • Every store matches the store master                                     │
│  • net_sales equals gross_sales minus discount_amount                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                               LOAD                                           │
│  • Save to data/processed/sales_analytics.csv                               │
│  • Load to SQLite database: data/retail_analytics.db                        │
│  • Table name: sales_analytics                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     QUERY / EVALUATE REQUIREMENTS                            │
│  • Top 10 products by net sales                                             │
│  • Monthly performance vs targets                                           │
│  • Regional sales analysis                                                  │
│  • Sales by region                                                          │
│  • Sales by category                                                        │
│  • Goal compliance by store                                                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Block Descriptions

| Block | Input | Responsibility | Output | Possible Failure |
|-------|-------|----------------|--------|------------------|
| Extract | Raw files (CSV, JSON, XML) | Read data into DataFrames | DataFrames with common schema | File not found, parse error |
| Profile | DataFrames | Analyze data quality | Profiling report | None |
| Clean/Harmonize | DataFrames | Fix data issues | Cleaned DataFrames | Data type conversion error |
| Transform/Integrate | Cleaned DataFrames + Reference tables | Join and calculate | Integrated DataFrame | Join key mismatch |
| Validate | Integrated DataFrame | Verify data quality | Validation result | Quality rule violation |
| Load | Integrated DataFrame | Save to CSV and SQLite | CSV file + DB table | Database connection error |
| Query | SQLite database | Execute analytical queries | Query results | SQL syntax error |

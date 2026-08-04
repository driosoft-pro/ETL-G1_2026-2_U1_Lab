# Retail Analytics Platform

**Course:** ETL Processes & Data Engineering  
**Term:** 2026-2  
**Group:** G1

---

## Overview

This repository contains a complete retail data analytics platform developed across two complementary labs:

- **Lab 1A** (`1a/`) — Business requirements analysis, KPIs, user stories, and dashboard wireframe.
- **Lab 1B** (`1b/`) — ETL pipeline implementation that extracts, transforms, and loads retail transaction data into a SQLite database.

Together, they form a unified solution for centralizing sales, promotions, and commercial goals data from three branches in Colombia (Cali, Bogota, Medellin) to enable data-driven decision-making.

---

## Problem

Sales, inventory, and product data are scattered across spreadsheets and different systems (POS, Promotion System, Commercial Goals System), making it difficult for managers to get a quick, reliable view of store performance and make timely, data-driven decisions.

---

## Objectives

- Build a centralized analytical platform.
- Integrate sales, promotions, and commercial goals data through a robust ETL pipeline.
- Answer key business questions through SQL queries.
- Enable data-driven decision-making for store managers.

---

## Repository Structure

```
Activities/1-2/
│
├── README.md                    # This file - unified project overview
│
├── 1a/                          # Lab 1A - Business Requirements Analysis
│   ├── README.md                # Lab 1A details
│   ├── informe.pdf              # Full compiled report
│   ├── referencias.bib          # Bibliography
│   ├── Doc/                     # LaTeX source files
│   ├── figures/                 # Wireframes and diagrams
│   └── tables/                  # Table images
│
└── 1b/                          # Lab 1B - ETL Pipeline
    ├── README.md                # Lab 1B details
    ├── requirements.txt         # Python dependencies
    ├── .env.example             # Environment template
    ├── data/raw/                # Source data files
    ├── database/                # SQLite initialization
    ├── docs/                    # Sprint plan, report template
    ├── src/                     # ETL pipeline code
    ├── tests/                   # Test files
    └── logs/                    # Execution logs
```

---

## How It Works

### Step 1: Business Analysis (Lab 1A)

The first phase defines the business context:
- Problem identification and objectives
- KPIs for store performance tracking
- User stories for platform features
- Dashboard wireframe design
- Data requirements mapping

See [`1a/README.md`](1a/README.md) for details.

### Step 2: ETL Pipeline (Lab 1B)

The second phase implements the technical solution:

1. **Extract** — Read data from CSV, JSON, and XML
2. **Profile** — Analyze data quality (nulls, duplicates, types)
3. **Clean** — Fix data issues
4. **Transform** — Integrate with reference tables, calculate metrics
5. **Validate** — Ensure data integrity
6. **Load** — Export to CSV and SQLite database
7. **Query** — Answer business questions

See [`1b/README.md`](1b/README.md) for details.

---

## Quick Start

### Prerequisites

- Python 3.12+
- pip

### Installation

```bash
# Navigate to Lab 1B
cd 1b

# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
# .venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
```

### Run the Pipeline

```bash
python -m src.main
```

The pipeline will:
1. Create a SQLite database at `data/retail_analytics.db`
2. Process all retail transaction data
3. Generate analysis results

---

## Data Sources

| Branch | Format | File |
|---|---|---|
| Cali | CSV | `1b/data/raw/sales_cali.csv` |
| Bogota | JSON | `1b/data/raw/sales_bogota.json` |
| Medellin | XML | `1b/data/raw/sales_medellin.xml` |

### Reference Data

| File | Description |
|---|---|
| `1b/data/raw/products.csv` | Product master and category |
| `1b/data/raw/stores.csv` | Branch, city, and region |
| `1b/data/raw/promotions.csv` | Campaign dates and discount percentages |
| `1b/data/raw/monthly_targets.csv` | Sales goal for each branch and month |

---

## KPIs

| KPI | Description |
|-----|-------------|
| Total Revenue | Total value of sales across all channels |
| Sales by Store | Performance comparison across branches |
| Sales by Region | Geographic analysis of commercial activity |
| Sales by Category | Revenue contribution by product category |
| Top 10 Best-Selling Products | Most in-demand products for inventory decisions |
| Sales Growth (%) | Period-over-period comparison |
| Goal Compliance Percentage | Degree of commercial objective achievement |
| Sales Increase by Promotion | Impact of promotional campaigns on sales |
| Average Order Value | Average transaction value for operational tracking |

---

## Team

| Member | Role | Responsibilities |
|--------|------|------------------|
| [Deyton Riascos Ortiz](https://github.com/drzriascos) | **Project Manager & Tech Lead** | Coordinate the project, architecture, main.py, module integration, Git, PR review, final validations |
| [Samuel Izquierdo Bonilla](https://github.com/samuelizquierdob) | **ETL - Extract & Profile** | extract.py, profile.py, CSV/JSON/XML reading, profiling, and findings documentation |
| [Daniel David Garcia Restrepo](https://github.com/danielgarcia260) | **ETL - Clean & Transform** | clean.py, transform.py, master table integration, metrics calculation, and business objectives |
| [Mauricio Taborda Gongora](https://github.com/mauriciotaborda) | **Quality & Analytics** | validate.py, load.py, queries.py, testing, and compliance evidence |

---

## Technologies

- Python 3.12+
- pandas
- SQLite (via sqlite3 standard library)
- xml.etree.ElementTree
- json
- logging
- pathlib
- python-dotenv
- Git + GitHub

---

## References

- DAMA International. *DAMA-DMBOK: Data Management Body of Knowledge*. 2nd Edition, Technics Publications, 2017.
- Project Management Institute. *A Guide to the Project Management Body of Knowledge (PMBOK Guide)*. 7th Edition, PMI, 2021.
- Kimball, R. & Ross, M. *The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling*. 3rd Edition, Wiley, 2013.
- Inmon, W.H. *Building the Data Warehouse*. 4th Edition, Wiley, 2005.

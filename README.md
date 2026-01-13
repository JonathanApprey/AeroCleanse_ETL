# AeroCleanse ETL Pipeline ✈️

**AeroCleanse** is a robust, Data Engineering portfolio project designed to simulate a real-world DoD Maintenance, Repair, and Overhaul (MRO) data pipeline. It demonstrates the end-to-end process of ingesting raw, unstructured aircraft maintenance logs, cleaning them using advanced Regex patterns, and loading verified data into a relational database for analytics.

## 🚀 Project Overview

In the aviation and defense sectors, data often arrives in "messy", inconsistent formats from various field technicians and legacy systems. This project solves that problem by:

1.  **Ingesting** raw maintenance logs (CSV & JSON) from a simulated landing zone.
2.  **Transforming** the data:
    *   Standardizing diverse date formats (ISO, US, Text) to a unified standard.
    *   Using **Regular Expressions (Regex)** to hunt down and extract critical error codes embedded in free-text descriptions.
    *   Validating data integrity (e.g., ensuring valid Aircraft IDs).
3.  **Loading** refined data into a SQL database for reporting.
4.  **Analyzing** fleet readiness and identifying top maintenance issues.

## 🛠️ Tech Stack using Python 3.11

*   **Core Logic:** Python (Pandas, NumPy)
*   **Data Cleaning:** Regular Expressions (re), dateutil
*   **Database:** SQLite, SQLAlchemy
*   **Testing:** pytest
*   **Data Generation:** Faker (for synthetic test data)

## 📁 Repository Structure
```
AeroCleanse_ETL/
├── data/
│   ├── raw/             # Landing zone for incoming files
│   └── processed/       # Archive for successfully processed files
├── src/
│   ├── data_generator.py # Simulates raw field data (Errors, messy dates)
│   ├── db_setup.py       # Initializes the SQLite Schema
│   ├── etl_pipeline.py   # The core ETL engine
│   └── analytics.py      # Generates insights from the DB
├── tests/
│   └── test_etl.py       # Unit tests for cleaning logic
└── requirements.txt      # Project dependencies
```

## ⚡ How to Run

### 1. Setup Environment
```bash
git clone https://github.com/JonathanApprey/AeroCleanse_ETL.git
cd AeroCleanse_ETL
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python src/db_setup.py
```

### 3. Generate Mock Data
Create synthetic "messy" data to test the pipeline:
```bash
python src/data_generator.py
```

### 4. Run ETL Pipeline
Ingest, Clean, and Load the data:
```bash
python src/etl_pipeline.py
```

### 5. View Analytics
See the results of the processing:
```bash
python src/analytics.py
```

### 6. Run Tests
Verify system integrity:
```bash
pytest
```

## 🔍 Key Features Demonstrated
*   **Regex Extraction:** Parsing unstructured text to find pattern-based codes (e.g., `ERR-2025-AX99`).
*   **Defensive Coding:** Handling nulls, mixed date formats, and missing foreign keys without crashing.
*   **Schema Design:** 3rd Normalized Form database structure.
*   **Unit Testing:** ensuring reliability of critical cleaning functions.

---
*Built by [Jonathan Ekow Apprey](https://github.com/JonathanApprey) as a demonstration of Data Engineering competencies.*

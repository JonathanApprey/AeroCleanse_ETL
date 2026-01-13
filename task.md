# AeroCleanse ETL Pipeline - Task Checklist

- [x] **Project Setup**
    - [x] Create project directory structure (`data/raw`, `data/processed`, `src`, `tests`)
    - [x] Initialize git repository
    - [x] Create `requirements.txt` (pandas, sqlalchemy, pytest, faker)

- [x] **Mock Data Generation**
    - [x] Create `src/data_generator.py` to simulate aircraft maintenance logs
    - [x] Implement error injection (malformed dates, null values)
    - [x] Generate initial "raw" CSV/JSON files

- [x] **Database Design**
    - [x] Design Schema (Tables: `Aircraft`, `MaintenanceEvents`, `RefErrorCodes`)
    - [x] Create `src/db_setup.py` for SQLite initialization

- [x] **ETL Processing**
    - [x] **Extract**: Read files from `data/raw`
    - [x] **Transform**:
        - [x] Regex extraction of error codes from text descriptions
        - [x] Standardize date formats
        - [x] Validate mandatory fields
    - [x] **Load**: Insert cleaned data into SQLite
    - [x] Create `src/etl_pipeline.py`

- [x] **Analytics**
    - [x] Create SQL queries for "Top Maintenance Issues" and "Fleet Readiness"
    - [x] Write `src/analytics.py` to print a summary report

- [x] **Verification**
    - [x] Verify pipeline handles corrupt data gracefully (no crashes, logs errors)
    - [x] Confirm database integrity

import pandas as pd
import glob
import os
import json
import re
import shutil
import datetime
from sqlalchemy import create_engine
from dateutil import parser

# Configuration
RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
DB_URL = "sqlite:///maintenance.db"
ENGINE = create_engine(DB_URL)

def extract_data():
    """Reads all CSV and JSON files from the raw directory."""
    all_files = glob.glob(os.path.join(RAW_DIR, "*"))
    data_frames = []
    
    print(f"Found {len(all_files)} files to process.")
    
    for file_path in all_files:
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
                df['source_file'] = os.path.basename(file_path)
                data_frames.append(df)
            elif file_path.endswith('.json'):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                df = pd.DataFrame(data)
                df['source_file'] = os.path.basename(file_path)
                data_frames.append(df)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            
    if not data_frames:
        return pd.DataFrame()
        
    return pd.concat(data_frames, ignore_index=True)

def normalize_date(date_str):
    """Parses various date formats into YYYY-MM-DD or Returns None."""
    if pd.isna(date_str) or str(date_str).strip().upper() in ['N/A', '', 'NONE', 'NULL']:
        return None
    try:
        # dateutil parser is robust for many formats
        dt = parser.parse(str(date_str))
        return dt.date()
    except (ValueError, TypeError):
        return None

def extract_error_code(description):
    """Extracts ERR-YYYY-Code pattern using Regex."""
    if pd.isna(description):
        return None
    match = re.search(r'ERR-\d{4}-[A-Z0-9]+', str(description))
    if match:
        return match.group(0)
    return None

def transform_data(df):
    """Cleans and standardizes the dataframe."""
    if df.empty:
        return df

    # 1. Clean Aircraft IDs (Drop empty)
    initial_count = len(df)
    df = df[df['aircraft_id'].astype(bool)] # Remove empty strings/nulls
    df = df.dropna(subset=['aircraft_id'])
    print(f"Dropped {initial_count - len(df)} rows with missing Aircraft IDs.")

    # 2. Standardize Dates
    df['event_date'] = df['event_date'].apply(normalize_date)

    # 3. Extract Error Codes
    df['error_code'] = df['description'].apply(extract_error_code)
    
    # 4. Add Processed Timestamp
    df['processed_at'] = datetime.datetime.utcnow().date()
    
    return df

import traceback

def load_data(df):
    """Loads data into SQLite."""
    if df.empty:
        print("No data to load.")
        return
    
    try:
        df.to_sql('maintenance_logs', ENGINE, if_exists='append', index=False)
        print(f"Successfully loaded {len(df)} records into the database.")
    except Exception as e:
        print(f"Error loading to database: {e}")
        print(traceback.format_exc())

def archive_files():
    """Moves processed files to the processed directory."""
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    files = glob.glob(os.path.join(RAW_DIR, "*"))
    for f in files:
        try:
            shutil.move(f, os.path.join(PROCESSED_DIR, os.path.basename(f)))
        except Exception as e:
            print(f"Error archiving {f}: {e}")

def run_pipeline():
    print("--- Starting ETL Pipeline ---")
    
    # Extract
    raw_data = extract_data()
    
    # Transform
    cleaned_data = transform_data(raw_data)
    
    # Load
    load_data(cleaned_data)
    
    # Archive
    archive_files()
    
    print("--- Pipeline Completed ---")

if __name__ == "__main__":
    run_pipeline()

import pandas as pd
from sqlalchemy import create_engine

DB_URL = "sqlite:///maintenance.db"
ENGINE = create_engine(DB_URL)

def run_analytics():
    print("\n=== AeroCleanse Maintenance Analytics Report ===\n")
    
    # 1. Total Records
    total = pd.read_sql("SELECT count(*) as count FROM maintenance_logs", ENGINE)
    print(f"Total Maintenance Events Processed: {total['count'][0]}")
    
    # 2. Top 5 Most Frequent Error Codes
    print("\n--- Top 5 Frequent Error Codes ---")
    top_errors = pd.read_sql("""
        SELECT error_code, COUNT(*) as frequency 
        FROM maintenance_logs 
        WHERE error_code IS NOT NULL 
        GROUP BY error_code 
        ORDER BY frequency DESC 
        LIMIT 5
    """, ENGINE)
    print(top_errors.to_string(index=False))
    
    # 3. Events by Aircraft Model
    print("\n--- Maintenance Events by Aircraft Model ---")
    # Extract model from aircraft_id (Assuming format MODEL-ID)
    events_by_model = pd.read_sql("""
        SELECT 
            substr(aircraft_id, 1, instr(aircraft_id, '-') - 1) as model,
            COUNT(*) as event_count
        FROM maintenance_logs
        GROUP BY model
        ORDER BY event_count DESC
    """, ENGINE)
    print(events_by_model.to_string(index=False))
    
    # 4. Recent Maintenance Activity
    print("\n--- Recent Activity (Last 5 Events) ---")
    recent = pd.read_sql("""
        SELECT event_date, aircraft_id, error_code, description
        FROM maintenance_logs
        ORDER BY event_date DESC
        LIMIT 5
    """, ENGINE)
    print(recent.to_string(index=False))

if __name__ == "__main__":
    run_analytics()

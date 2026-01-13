import pytest
import pandas as pd
import sys
import os

# Add src to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from etl_pipeline import extract_error_code, normalize_date, transform_data

def test_extract_error_code():
    # Test valid codes
    assert extract_error_code("System failed with [ERR-2024-AB12] code.") == "ERR-2024-AB12"
    assert extract_error_code("ERR-2023-XY99") == "ERR-2023-XY99"
    
    # Test invalid codes
    assert extract_error_code("System normal.") is None
    assert extract_error_code("Error code 2024-AB12") is None # Missing prefix
    assert extract_error_code(None) is None
    assert extract_error_code(12345) is None

def test_normalize_date():
    # Test various formats
    assert str(normalize_date("2024-01-31")) == "2024-01-31"
    assert str(normalize_date("01/31/2024")) == "2024-01-31"
    assert str(normalize_date("31-Jan-2024")) == "2024-01-31"
    
    # Test invalid inputs
    assert normalize_date("Not a date") is None
    assert normalize_date("N/A") is None
    assert normalize_date(None) is None

def test_transform_data():
    # Create sample data
    data = {
        'aircraft_id': ['F-16-100', '', None, 'C-130-200'],
        'event_date': ['2024-01-01', 'N/A', '01-01-2024', '2024/01/01'],
        'description': ['Error [ERR-2024-A1] found', 'Clean', 'Clean', 'Fault [ERR-2023-B2]'],
        'technician': ['Tech A', 'Tech B', 'Tech C', 'Tech D']
    }
    df = pd.DataFrame(data)
    
    cleaned = transform_data(df)
    
    # Check that rows with missing aircraft_id are dropped (empty string and None)
    assert len(cleaned) == 2
    assert 'F-16-100' in cleaned['aircraft_id'].values
    assert 'C-130-200' in cleaned['aircraft_id'].values
    
    # Check extractions
    assert cleaned.iloc[0]['error_code'] == "ERR-2024-A1"
    assert cleaned.iloc[1]['error_code'] == "ERR-2023-B2"
    
    # Check dates
    assert str(cleaned.iloc[0]['event_date']) == "2024-01-01"

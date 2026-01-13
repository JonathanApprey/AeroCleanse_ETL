import random
import csv
import json
import os
import datetime
from faker import Faker

fake = Faker()

def generate_error_code():
    """Generates a random error code pattern."""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return f"ERR-{random.randint(2020, 2025)}-{random.choice(chars)}{random.choice(chars)}{random.randint(10, 99)}"

def generate_dirty_date():
    """Returns a date string in various formats to simulate messy data."""
    dt = fake.date_between(start_date='-2y', end_date='today')
    formats = [
        "%Y-%m-%d",   # Standard
        "%m-%d-%Y",   # US
        "%Y/%m/%d",   # Slashes
        "%d-%b-%Y"    # Day-MonthName-Year
    ]
    if random.random() < 0.1:
        return "N/A" # Simulate missing date
    return dt.strftime(random.choice(formats))

def generate_description():
    """Generates a maintenance description, optionally embedding an error code."""
    desc = fake.sentence(nb_words=10)
    if random.random() < 0.7:  # 70% chance of having an error code
        # Embed error code somewhere in the text
        parts = desc.split()
        insert_idx = random.randint(0, len(parts)-1)
        parts.insert(insert_idx, f"[{generate_error_code()}]")
        desc = " ".join(parts)
    return desc

def generate_aircraft_data(num_records=100):
    """Generates synthetic aircraft maintenance logs."""
    data = []
    aircraft_models = ['F-16', 'C-130', 'B-52', 'F-35', 'A-10']
    
    for _ in range(num_records):
        record = {
            "aircraft_id": f"{random.choice(aircraft_models)}-{random.randint(1000, 9999)}",
            "technician": fake.name(),
            "event_date": generate_dirty_date(),
            "description": generate_description(),
            "location": random.choice(["Base A", "Base B", "Forward Operating Base"]),
            "parts_replaced": random.choice(["Filter", "Valve", "Sensor", "None", "Gasket"])
        }
        
        # Inject nulls/bad data
        if random.random() < 0.05:
            record["aircraft_id"] = "" # Missing ID
            
        data.append(record)
    return data

def save_data(data, format_type='csv'):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = "data/raw"
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"{output_dir}/maintenance_log_{timestamp}.{format_type}"
    
    if format_type == 'csv':
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    elif format_type == 'json':
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
            
    print(f"Generated {len(data)} records in {filename}")

if __name__ == "__main__":
    # Generate a CSV batch
    csv_data = generate_aircraft_data(50)
    save_data(csv_data, 'csv')
    
    # Generate a JSON batch
    json_data = generate_aircraft_data(30)
    save_data(json_data, 'json')

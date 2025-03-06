from pathlib import Path
import csv
import json
import toml

EXPORT_DIR = Path("./exports/intermediate")

def save_hourly_data_to_file(data: dict):
    """Save hourly data to a CSV file."""
    if not EXPORT_DIR.exists():
        EXPORT_DIR.mkdir(parents=True)
    file_path = EXPORT_DIR / "hourly_data.csv"
    with open(file_path, "a") as file:
        file.write(f"{data['timestamp']},{data['flow_rate']},{data['cod']},{data['water_quality']}\n")
    print(f"Data saved to {file_path}")

def save_hourly_data_to_csv(data: dict):
    """Save hourly data to a CSV file."""
    # Ensure the export directory exists
    if not EXPORT_DIR.exists():
        EXPORT_DIR.mkdir(parents=True)

    file_path = EXPORT_DIR / "hourly_data.csv"

    # Write or append to the CSV file
    with open(file_path, mode="a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # Write the header if the file is empty
        if file_path.stat().st_size == 0:
            writer.writerow(["timestamp", "flow_rate", "cod", "water_quality"])
        # Write the data
        writer.writerow([data["timestamp"], data["flow_rate"], data["cod"], data["water_quality"]])
    
    print(f"Hourly data saved to {file_path}"
    

def save_hourly_data_to_json(data: dict):
    """Save hourly data to a JSON file."""
    # Ensure the export directory exists
    if not EXPORT_DIR.exists():
        EXPORT_DIR.mkdir(parents=True)

    file_path = EXPORT_DIR / "hourly_data.json"

    # Append the data to the JSON file
    if file_path.exists():
        with open(file_path, mode="r+", encoding="utf-8") as jsonfile:
            existing_data = json.load(jsonfile)
            existing_data.append(data)
            jsonfile.seek(0)
            json.dump(existing_data, jsonfile, indent=4)
    else:
        with open(file_path, mode="w", encoding="utf-8") as jsonfile:
            json.dump([data], jsonfile, indent=4)

    print(f"Hourly data saved to {file_path}")
    

def save_hourly_data_to_toml(data: dict):
    """
    Save hourly data to a TOML file.

    Parameters:
        data (dict): Dictionary containing hourly data fields such as
                     'timestamp', 'flow_rate', 'cod', and 'water_quality'.

    Example data:
        {
            "timestamp": "2025-03-05T13:00:00",
            "flow_rate": 120.5,
            "cod": 38.1,
            "water_quality": "good"
        }
    """
    # Ensure the export directory exists
    if not EXPORT_DIR.exists():
        EXPORT_DIR.mkdir(parents=True)

    file_path = EXPORT_DIR / "hourly_data.toml"

    # Load existing data from the TOML file if it exists
    existing_data = {}
    if file_path.exists():
        with open(file_path, mode="r", encoding="utf-8") as tomlfile:
            existing_data = toml.load(tomlfile)

    # Add the new entry to the existing data
    if "hourly_data" not in existing_data:
        existing_data["hourly_data"] = []
    existing_data["hourly_data"].append(data)

    # Save the updated data back to the TOML file
    with open(file_path, mode="w", encoding="utf-8") as tomlfile:
        toml.dump(existing_data, tomlfile)

    print(f"Hourly data saved to {file_path}")
    
def log_export_operation(message: str):
    """Log operations in export.log."""
    file_path = EXPORT_DIR / "export.log"
    with open(file_path, mode="a", encoding="utf-8") as logfile:
        logfile.write(f"{message}\n")

def list_export_files():
    """
    Returns a list of file names in the export directory.
    """
    if EXPORT_DIR.exists():
        return [file.name for file in EXPORT_DIR.iterdir()]
    else:
        return None

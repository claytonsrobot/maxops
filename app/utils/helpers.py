from pathlib import Path
import csv
import json
import toml

EXPORT_DIR = Path("./exports/intermediate")

def ensure_dir():
    # Ensure the export directory exists
    if not EXPORT_DIR.exists():
        EXPORT_DIR.mkdir(parents=True)

def save_hourly_data(data: dict):
    save_data_to_csv(data, file_path = EXPORT_DIR / "hourly_data.csv")
    save_data_to_json(data, file_path = EXPORT_DIR / "hourly_data.json")
    save_data_to_toml(data, file_path = EXPORT_DIR / "hourly_data.toml")

def save_daily_data(data: dict):
    save_data_to_csv(data, file_path = EXPORT_DIR / "daily_data.csv")
    save_data_to_json(data, file_path = EXPORT_DIR / "daily_data.json")
    save_data_to_toml(data, file_path = EXPORT_DIR / "daily_data.toml")


def save_data_to_csv(data: dict, file_path):
    """Save hourly data to a CSV file."""
    ensure_dir()

    # Write or append to the CSV file
    with open(file_path, mode="a+", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # Write the header if the file is empty
        if file_path.stat().st_size == 0:
            writer.writerow([key for key in data.keys()])
        else:
            
            # check if existing headers/keys match data.keys()
            csvfile.seek(0)
            reader = csv.reader(csvfile)
            try:
                column_headers = next(reader)
                if column_headers == list(data.keys()):
                    print("The existing CSV column names match data.keys()")
                else:
                    print("WARNING: The existing CSV column names DO NOT match data.keys()")
            except StopIteration:
                print("ERROR: The file appears to be empty, but stat() reported otherwise.")
                        # Write the data
        write_dict(writer, data)
    print(f"Data saved to {file_path}")
    
def write_dict(writer, data):
    """
    Writes all keys and values from a dictionary to a CSV file using the writer object.
    
    Args:
        writer: A csv.writer object.
        data: A dictionary containing key-value pairs to write.
    """
    writer.writerow([value for key, value in data.items()])
                     
def save_data_to_json(data: dict, file_path):
    """Save hourly data to a JSON file."""
    ensure_dir()

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

    print(f"Data saved to {file_path}")
    

def save_data_to_toml(data: dict, file_path):
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
    ensure_dir()


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

    print(f"Data saved to {file_path}")
    
def log_export_operation(message: str):
    """Log operations in export.log."""
    file_path = EXPORT_DIR / "export.log"
    with open(file_path, mode="a", encoding="utf-8") as logfile:
        logfile.write(f"{message}\n")


def list_export_files():
    """
    Lists all files in the export directory.

    Returns:
        list: A list of file names in the export directory.
    """
    if EXPORT_DIR.exists() and EXPORT_DIR.is_dir():
        # Return a list of file names (not paths) in the directory
        return [file.name for file in EXPORT_DIR.iterdir() if file.is_file()]
    return []  # Return an empty list if the directory doesn't exist or is empty


def clear_export_directory():
    """
    Clears all files in the export directory.

    Returns:
        bool: True if the files were successfully deleted, False if the directory does not exist.
    """
    if EXPORT_DIR.exists() and EXPORT_DIR.is_dir():
        try:
            # Iterate through and delete each file in the directory
            for file in EXPORT_DIR.iterdir():
                if file.is_file():
                    file.unlink()  # Delete the file
            return True  # Return True when the directory is successfully cleared
        except Exception as e:
            print(f"Error clearing export directory: {e}")  # Handle unexpected errors
            return False
    return False  # Return False if the directory does not exist

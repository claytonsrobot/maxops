import json
import os
import FreeSimpleGUI as sg

def load_data_from_json(file_path):
    """Loads data from a JSON file."""
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    else:
        sg.popup_error(f"File '{file_path}' not found!")
        return []

def create_table_layout(data):
    """Creates a table layout from the loaded JSON data."""
    # Define headers based on the keys of the first entry, if data exists
    if data:
        headers = list(data[0].keys())
        values = [[entry[key] for key in headers] for entry in data]
    else:
        headers = ["No Data Found"]
        values = []
    return headers, values

# Main program
def outfall_known_window():
    json_file = os.path.join("exports","intermediate" ,"daily_outfall_data.json")
    data = load_data_from_json(json_file)

    # Create headers and table data
    headers, table_data = create_table_layout(data)

    # Define the layout for the PySimpleGUI window
    layout = [
        [sg.Text("Daily Outfall Data Submissions", font=("Helvetica", 16))],
        [sg.Table(
            values=table_data,
            headings=headers,
            justification="center",
            auto_size_columns=False,  # Turn off auto-sizing to control column widths
            col_widths=[len(header) -2 for header in headers],  # Dynamically set minimal width
            display_row_numbers=True,
            num_rows=20,
            key="-TABLE-"
        )],
        [sg.Button("Refresh"), sg.Button("Close")]
    ]

    # Create the window
    window = sg.Window("Outfall Data Viewer", layout, resizable=True)

    # Event loop
    while True:
        event, _ = window.read()
        if event == sg.WINDOW_CLOSED or event == "Close":
            break
        elif event == "Refresh":
            # Reload data on refresh
            data = load_data_from_json(json_file)
            headers, table_data = create_table_layout(data)
            window["-TABLE-"].update(values=table_data)
    window.close()

# Main program
def hourly_known_window():
    json_file = os.path.join("exports","intermediate" ,"hourly_data.json")
    data = load_data_from_json(json_file)

    # Create headers and table data
    headers, table_data = create_table_layout(data)

    # Define the layout for the PySimpleGUI window
    layout = [
        [sg.Text("Hourly Data Submissions", font=("Helvetica", 16))],
        [sg.Table(
            values=table_data,
            headings=headers,
            justification="center",
            auto_size_columns=False,  # Turn off auto-sizing to control column widths
            col_widths=[len(header) -2 for header in headers],  # Dynamically set minimal width
            display_row_numbers=True,
            num_rows=20,
            key="-TABLE-"
        )],
        [sg.Button("Refresh"), sg.Button("Close")]
    ]

    # Create the window
    window = sg.Window("Hourly Data Viewer", layout, resizable=True)

    # Event loop
    while True:
        event, _ = window.read()
        if event == sg.WINDOW_CLOSED or event == "Close":
            break
        elif event == "Refresh":
            # Reload data on refresh
            data = load_data_from_json(json_file)
            headers, table_data = create_table_layout(data)
            window["-TABLE-"].update(values=table_data)
    window.close()

if __name__ == "__main__":
    outfall_known_window()

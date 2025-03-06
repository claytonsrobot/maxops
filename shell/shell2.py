import cmd2
import subprocess
from pathlib import Path
import requests
import argparse
import json

from shell.query import run_query  # Import the tutorial function
from shell.tutorial import run_tutorial  # Import the tutorial function
from shell.batch_processor import process_batch  # Import batch processing function
#from shell.command_registry import register_commands  # Import command registration function

# Path configuration for your project
EXPORT_DIR = Path("./exports/intermediate")

class ShellApp(cmd2.Cmd):
    """Interactive shell for testing, spoofing, and running the web app."""

    # Shell prompt
    prompt = "maxops> "

    def __init__(self):
        super().__init__()
        #register_commands(self)  
        
    # Add the tutorial command
    def do_tutorial(self, args):
        """Launch the interactive tutorial to learn about the project."""
        run_tutorial()
        
    # Add the query command
    def do_query(self, args):
        """Launch the interactive query tool to create batch scripts."""
        run_query()
        

    # === Command: Run Web App ===
    run_webapp_parser = argparse.ArgumentParser(description="Run the FastAPI web app.")
    @cmd2.with_argparser(run_webapp_parser)
    def do_run_webapp(self, args):
        """Start the FastAPI web app (in development mode)."""
        try:
            print("Starting the web app...")
            subprocess.run(["uvicorn", "app.main:app", "--reload"], check=True)
        except KeyboardInterrupt:
            print("\nWeb app stopped by user.")
        except Exception as e:
            print(f"Error starting the web app: {e}")

    # === Command: Spoof Hourly Data ===
    spoof_hourly_parser = argparse.ArgumentParser(description="Spoof hourly data for testing.")
    spoof_hourly_parser.add_argument("timestamp", type=str, help="Timestamp in ISO format, e.g., 2025-03-05T08:00:00")
    spoof_hourly_parser.add_argument("flow_rate", type=float, help="Flow rate value.")
    spoof_hourly_parser.add_argument("cod", type=float, help="COD value.")
    spoof_hourly_parser.add_argument("water_quality", type=str, help="Water quality (e.g., excellent, good, fair).")
    @cmd2.with_argparser(spoof_hourly_parser)
    def do_spoof_hourly(self, args):
        """Spoof hourly data and send it to the API."""
        try:
            data = {
                "timestamp": args.timestamp,
                "flow_rate": args.flow_rate,
                "cod": args.cod,
                "water_quality": args.water_quality
            }
            response = requests.post("http://localhost:8000/submit-hourly", data=data)
            print(f"Server response: {response.json()}")
        except Exception as e:
            print(f"Error spoofing hourly data: {e}")

    # === Command: Spoof Daily Data ===
    spoof_daily_parser = argparse.ArgumentParser(description="Spoof daily data for testing.")
    spoof_daily_parser.add_argument("date", type=str, help="Date in YYYY-MM-DD format.")
    spoof_daily_parser.add_argument("clarifier_status", type=str, help="Clarifier status (e.g., operational, under maintenance).")
    spoof_daily_parser.add_argument("observations", type=str, help="Daily observations.")
    @cmd2.with_argparser(spoof_daily_parser)
    def do_spoof_daily(self, args):
        """Spoof daily summary data and send it to the API."""
        try:
            data = {
                "date": args.date,
                "clarifier_status": args.clarifier_status,
                "observations": args.observations
            }
            response = requests.post("http://localhost:8000/submit-daily", data=data)
            print(f"Server response: {response.json()}")
        except Exception as e:
            print(f"Error spoofing daily data: {e}")

    # === Command: List Export Files ===
    list_exports_parser = argparse.ArgumentParser(description="List files in the export directory.")
    @cmd2.with_argparser(list_exports_parser)
    def do_list_exports(self, args):
        """List files in the export directory."""
        try:
            if EXPORT_DIR.exists():
                for file in EXPORT_DIR.iterdir():
                    print(f"Export file: {file.name}")
            else:
                print("Export directory does not exist.")
        except Exception as e:
            print(f"Error listing export files: {e}")

    # === Command: Clear Export Files ===
    clear_exports_parser = argparse.ArgumentParser(description="Clear all files in the export directory.")
    @cmd2.with_argparser(clear_exports_parser)
    def do_clear_exports(self, args):
        """Clear all files in the export directory."""
        try:
            if EXPORT_DIR.exists():
                for file in EXPORT_DIR.iterdir():
                    file.unlink()
                    print(f"Deleted: {file.name}")
                print("Export directory cleared.")
            else:
                print("Export directory does not exist.")
        except Exception as e:
            print(f"Error clearing export files: {e}")
    
    # === Command: Execute Batch Script ===
    # Add batch command
    def do_batch(self, args):
        """Execute commands from a batch script located in the batch directory."""
        batch_file_name = args.strip()
        if not batch_file_name:
            print("Usage: batch <batch_file_name>")
        else:
            process_batch(batch_file_name, self)
            
    # === Command: Test Recent Hourly Data ===
    test_recent_hourly_parser = argparse.ArgumentParser(description="Test the /api/recent-hourly endpoint.")
    @cmd2.with_argparser(test_recent_hourly_parser)
    def do_test_recent_hourly(self, args):
        """Test the /api/recent-hourly endpoint."""
        try:
            response = requests.get("http://localhost:8000/api/recent-hourly")
            data = response.json()
            print(json.dumps(data, indent=4))
        except Exception as e:
            print(f"Error testing recent hourly data: {e}")

    # === Command: Test Recent Daily Data ===
    test_recent_daily_parser = argparse.ArgumentParser(description="Test the /api/daily-summaries endpoint.")
    @cmd2.with_argparser(test_recent_daily_parser)
    def do_test_recent_daily(self, args):
        """Test the /api/daily-summaries endpoint."""
        try:
            response = requests.get("http://localhost:8000/api/daily-summaries")
            data = response.json()
            print(json.dumps(data, indent=4))
        except Exception as e:
            print(f"Error testing recent daily data: {e}")

    # === Command: Quit Shell ===
    quit_parser = argparse.ArgumentParser(description="Quit the shell.")
    @cmd2.with_argparser(quit_parser)
    def do_quit(self, args):
        """Exit the shell."""
        print("Exiting the shell. Goodbye!")
        return True
        
    # === Command: Query Guidance ===
    query_parser = argparse.ArgumentParser(description="Run query guidance, to generate a batch script.")
    @cmd2.with_argparser(query_parser)
    def do_query(self, args):
        """Exit the shell."""
        run_query()
        print("The query guidance is complete :)")
        return True
        
    # === Command: Tutorial ===
    tutorial_parser = argparse.ArgumentParser(description="Run tutorial, to better undestand the MaxOps program.")
    @cmd2.with_argparser(tutorial_parser)
    def do_tutorial(self, args):
        """Run the tutorial."""
        run_tutorial()
        print("The tutorial is complete!")
        return True
        

if __name__ == "__main__":
    ShellApp().cmdloop()

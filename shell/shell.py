import cmd2
import os
import subprocess
from pathlib import Path
import requests
import argparse
import json
import pprint
from datetime import datetime
import ast
import operator
import psutil
import readline

from shell.query import run_query  # Import the tutorial function
from shell.tutorial import run_tutorial  # Import the tutorial function
from shell.batch_processor import process_batch  # Import batch processing function
#from shell.command_registry import register_commands  # Import command registration function

import app.utils.helpers as helpers
#from app.utils.helpers import save_hourly_data_to_csv,save_hourly_data_to_json,save_hourly_data_to_toml, save_daily_data_to_csv,save_daily_data_to_json,save_daily_data_to_toml 


# Path configuration for your project
EXPORT_DIR = Path("./exports/intermediate")

class HistoryEntry:
    """Custom history item to store and display commands properly."""
    def __init__(self, command: str):
        self.command = command.strip()  # Ensure no trailing or leading whitespace

    def pr(self, idx: int, script: bool = False, expanded: bool = False, verbose: bool = False) -> str:
        """Format history for printing, ensuring clean and consistent output."""
        return f"{idx}: {self.command}"

    def __str__(self):
        return f"{'-'}: {self.command}"
        #return self.command

class ShellApp(cmd2.Cmd):
    """Interactive shell for testing, spoofing, and running the web app."""

    # Shell prompt
    #prompt = "maxops> "

    def __init__(self):
        super().__init__()
        self.prompt = "maxops> "
        self.user_vars = {}  
        self.vars = {}
        self.modules = {}
        self.context = {'self': self,
                        'pprint': pprint.pprint,
                        'list': list,
                        'str': str,
                        'int': int,
                        'float': float,
                        'dict': dict,
                        'dir': dir,
                        'set': set,
                        'tuple': tuple,
                        'len': len,
                        'sum': sum,
                        'min': min,
                        'max': max,
                        'sorted': sorted,
                        'type': type,
                        'range': range,
                        'enumerate': enumerate,
                        'zip': zip,
                        'map': map,
                        'filter': filter,
                        'any': any,
                        'all': all,
                        'abs': abs,
                        'round': round,
                        'repr': repr,}
        #print("ShellApp initialized!")
        #register_commands(self)  

        self.debug = True  # Set the default debug value to True
        
        # Set startup script - if the file does not exist, there will be problems
        #self.startup_script = os.path.join(os.path.dirname(__file__), "startup.txt")

        # Store command history
        history_dir = os.path.join(os.path.dirname(__file__), 'history')
        os.makedirs(history_dir, exist_ok=True)  # Ensure the directory exists
        self.persistent_history_file = os.path.join(history_dir, 'shell_history.txt')

        # Auto-load history from the file if it exists
        if os.path.exists(self.persistent_history_file):
            self._load_history()

    def _load_history(self):
        """Load commands from the persistent history file at startup."""
        try:
            if os.path.exists(self.persistent_history_file):
                with open(self.persistent_history_file, 'r', encoding='utf-8') as history_file:
                    for line in history_file:
                        command = line.strip()
                        if command:
                            self.history.append(HistoryEntry(command))  
                            readline.add_history(command)
                print(f"Loaded {len(self.history)} commands from history.")
            else:
                print("No history file found, starting with an empty history.")
        except Exception as e:
            self.perror(f"Error loading history: {e}")

    
    def postcmd(self, stop, statement):
        """Called after every command to append it to the history file."""
        try:
            full_command = statement.raw.strip()
            if full_command:
                with open(self.persistent_history_file, 'a', encoding='utf-8') as history_file:
                    history_file.write(full_command + '\n')

                self.history.append(HistoryEntry(full_command))  # Store properly
            else:
                print("Skipped saving empty or invalid command.")
        except Exception as e:
            self.perror(f"Error saving command to history: {e}")
        return stop

    # === Command: Test ===
    def do_test(self,line):
        "See CPU frequency."
        self.poutput("Test command executed successfully!")
        try:
            cpu_freq = psutil.cpu_freq()
            print("Current CPU Frequency:", round(cpu_freq.current),"hz, or so.") 
        except:
            pass

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
    spoof_hourly_parser.add_argument("-t","--timestamp", type=str, help="Timestamp in ISO format, e.g., 2025-03-05T08:00:00")
    spoof_hourly_parser.add_argument("-f","--flow_rate", type=float, help="Flow rate value.")
    spoof_hourly_parser.add_argument("-c","--cod", type=float, help="COD value.")
    spoof_hourly_parser.add_argument("-w","--water_quality", type=str, help="Water quality (e.g., excellent, good, fair).")
    """
    SAM says (three sheets in the hourly spreadsheet called Daily Data Spreashet (veriosn 1))
    
    Spreadsheet: Daily Data Spreashet (veriosn 1).xlsb
    Sheets: Hourly Flow, calriier flow, daily data
        - Hourly Flow
        -- Underflow and Ras are not put in manually but are calculated from entried in the Clarifer flow page
        -- Time
        -- Flow (influent)
        -- After wet well (flow)
        -- TOT WAS (MGD)
        -- 

        - Clarifier Flow
         ( requires groups and subgroups)
        -- Adds all underflows and then calcuates RAS. Underflow minus wasting equals RAS. 
        -- Influent flow on all aeration basins 
        -- Influent flow on secondary clarifiers
        -- Underflows from secondary clarifiers

        - Daily Data 
        Description: complex! partially figured from other sheet
        
    Spreadsheet: Maxson Hourly Effluent Flow (version 1)
        Frequency: Once per hour
        Future: could come from ovation automatically
        Sheets: New sheet per month
        Columns: Day of the month
        Rows: Each hour

    Spreadsheet: Maxson Hourly Prefinal COD Concentration 2023
        Frequency: Once per hour
        Future: could come from ovation automatically
        Sheets: New sheet every months
        Columns: Day of the month
        Rows: Each hour

    Spreadsheet: Outfall observations 2024
        Frequency: Once per day, first shit (7am-3pm)
        Future: Must be done manually, eyes on the outfall condition
        Sheets: New sheet every months
        Rows: Each Day
        Columns: Operator initials, time, yes no questionss
            questions: ["safe to make observation?", "flotable present?", "scum present?", "foam present?", "oil present?" ]

    """
    
    @cmd2.with_argparser(spoof_hourly_parser)
    def do_spoof_hourly(self, args):
        """Spoof hourly data and send it to the API."""

        if args.timestamp == "now":
            # overwrite
            print("timestamp is 'now', attempting to assign..")
            args.timestamp = self.nowtime()
            print(f"args.timestamp assigned as {args.timestamp}")
        else:
            pass
        
        """Capure args as data dictionary."""
        try:
            # if you chanage these keys and the order, and a relevant CSV file already exists, you should see: "WARNING: The existing CSV column names DO NOT match data.keys()"
            data = {
                "timestamp": args.timestamp,
                "flow_rate": args.flow_rate,
                "cod": args.cod,
                "water_quality": args.water_quality
            }
        except:
            print(f"Error spoofing hourly data: {e}")
            data = None
            print("Args not present")

        if data is not None:
            try:
                response = requests.post("http://localhost:8000/submit-hourly", data=data)
                print(f"Server response: {response.json()}")
            except Exception as e:
                print(f"Error spoofing hourly data: {e}")
                print("Web app not running, defaulting to local export.")

                helpers.save_hourly_data(data)
                #helpers.save_hourly_data_to_json(data)
                #helpers.save_hourly_data_to_toml(data)
                #helpers.save_hourly_data_to_csv(data)

    # === Command: Spoof Daily Data ===
    spoof_daily_parser = argparse.ArgumentParser(description="Spoof daily data for testing.")
    spoof_daily_parser.add_argument("-t","--timestamp", type=str, help="Timestamp in ISO format, e.g., 2025-03-05T08:00:00")
    #spoof_daily_parser.add_argument("-d","--date", type=str, help="Date in YYYY-MM-DD format.")
    spoof_daily_parser.add_argument("-c","--clarifier_status", type=str, help="Clarifier status (e.g., operational, under maintenance).")
    spoof_daily_parser.add_argument("-o","--observations", type=str, help="Daily observations.")
    @cmd2.with_argparser(spoof_daily_parser)
    def do_spoof_daily(self, args):
        """Spoof daily summary data and send it to the API."""

        if args.timestamp == "now":
            # overwrite
            print("timestamp is 'now', attempting to assign..")
            args.timestamp = self.nowtime()
            print(f"args.timestamp assigned as {args.timestamp}")
        else:
            pass
    
        try:
            # if you chanage these keys and the order, and a relevant CSV file already exists, you should see: "WARNING: The existing CSV column names DO NOT match data.keys()"
            data = {
                "timestamp": args.timestamp,
                "clarifier_status": args.clarifier_status,
                "observations": args.observations
            }
        except:
            print(f"Error spoofing hourly data: {e}")
            data = None
            print("Args not present")

        if data is not None:
            try:
                response = requests.post("http://localhost:8000/submit-daily", data=data)
                print(f"Server response: {response.json()}")
            except Exception as e:
                print(f"Error spoofing daily data: {e}")
                print("Web app not running, defaulting to local export.")

                helpers.save_daily_data(data)
                #helpers.save_daily_data_to_json(data)
                #helpers.save_daily_data_to_toml(data)
                #helpers.save_daily_data_to_csv(data)

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
        batch_filename=run_query()
        print("The query guidance is complete :)")
        return None
        
    # === Command: Tutorial ===
    tutorial_parser = argparse.ArgumentParser(description="Run tutorial, to better undestand the MaxOps program.")
    @cmd2.with_argparser(tutorial_parser)
    def do_tutorial(self, args):
        """Run the tutorial."""
        run_tutorial()
        print("The tutorial is complete!")
        #self.do_quit()
        return None
    
    # === Command: Now Time ===
    now_parser = argparse.ArgumentParser(description="Print Now time, to be easily copied or assigned to a spoof input.")
    @cmd2.with_argparser(now_parser)
    def do_now(self, args):
        """Calculate the current time."""
        now_time = self.nowtime()
        #print(f"{now_time}")
        self.poutput(f"{now_time}")
        #return None
    def nowtime(self):
        now_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        return now_time


    # === Command: print ===
    def do_print(self, args):
        if args:
            self.poutput(f"{args}")
        else:
            self.poutput("")


    def do_show(self, _):
        """Show all variables."""
        for key, value in self.vars.items():
            self.poutput(f"{key} = {value}")

    def do_eval(self, args):
        """Evaluate an expression using stored variables."""
        try:
            expr = self._substitute_vars(args)
            result = self._safe_eval(expr, self.context)
            self.poutput(f"{args} = {result}")
        except Exception as e:
            self.poutput(f"Error evaluating expression: {str(e)}")

    def _substitute_vars(self, expression):
        """Substitute variables in the expression with their values."""
        for key, value in self.vars.items():
            expression = expression.replace(key, value)
        return expression

    def _safe_eval(self, expression, context):
        """Safely evaluate an expression using ast and operator modules."""
        # Define allowed operators
        allowed_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.BitXor: operator.xor,
            ast.USub: operator.neg,
        }

        def _eval(node, context):
            if isinstance(node, ast.Constant):  # <number>
                return node.n
            elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
                return allowed_operators[type(node.op)](_eval(node.left, context), _eval(node.right, context))
            elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
                return allowed_operators[type(node.op)](_eval(node.operand, context))
            elif isinstance(node, ast.Name):  # <variable>
                return context[node.id]
            elif isinstance(node, ast.Attribute):  # <object.attribute>
                value = _eval(node.value, context)
                return getattr(value, node.attr)
            elif isinstance(node, ast.Call):  # <function call>
                func = _eval(node.func, context)
                args = [_eval(arg, context) for arg in node.args]
                return func(*args)
            elif isinstance(node, ast.Subscript):  # <variable>[<index>]
                value = _eval(node.value, context)
                if isinstance(node.slice, ast.Index):
                    index = _eval(node.slice.value, context)
                else:
                    index = _eval(node.slice, context)
                return value[index]
            else:
                raise TypeError(node)

        node = ast.parse(expression, mode='eval').body
        return _eval(node, context)


if __name__ == "__main__":
    app = ShellApp()
    app.cmdloop()

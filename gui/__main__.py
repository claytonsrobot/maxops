# __main__.py
from gui.gui import main

def cli_entry():
    try:
        # Launch the gui
        main() 
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    cli_entry()
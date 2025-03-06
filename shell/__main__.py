from cmd2 import Cmd
from shell.command_registry import (
    run_webapp,
    spoof_hourly,
    spoof_daily,
    list_exports,
    clear_exports,
    batch,
)
from shell.query import run_query  # Import the tutorial function
from shell.tutorial import run_tutorial  # Import the tutorial function

class ShellApp(Cmd):
    """Interactive shell for managing the web app and running batch commands."""

    def __init__(self):
        super().__init__()
        self._register_commands()

    def _register_commands(self):
        """Attach commands to the shell instance."""
        self.do_run_webapp = run_webapp
        self.do_spoof_hourly = spoof_hourly
        self.do_spoof_daily = spoof_daily
        self.do_list_exports = list_exports
        self.do_clear_exports = clear_exports
        self.do_batch = batch
        self.do_tutorial = run_tutorial
        self.do_query = run_query


if __name__ == "__main__":
    # Create a shell instance and start the command loop
    shell = ShellApp()
    shell.cmdloop()

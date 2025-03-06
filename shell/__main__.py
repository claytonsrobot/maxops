from cmd2 import Cmd
from shell.command_registry import register_commands

class ShellApp(Cmd):
    """Interactive shell for managing the web app and running batch commands."""

    def __init__(self):
        super().__init__()
        register_commands(self)


if __name__ == "__main__":
    # Create a shell instance and start the command loop
    shell = ShellApp()
    shell.cmdloop()

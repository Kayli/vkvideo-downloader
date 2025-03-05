import sys
from .cli_app import CLIApp

if __name__ == '__main__':
    cli_app = CLIApp()
    exit_code = cli_app.run()
    if exit_code != 0:
        sys.exit(exit_code)

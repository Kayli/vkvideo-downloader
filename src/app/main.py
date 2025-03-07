import sys
from enum import IntEnum
from typing import Optional, List

from .cli_app import CLIApp, CLIAppError
from .factory import Factory

class ExitCode(IntEnum):
    """
    Enum representing exit codes for the CLI application.
    
    Follows standard Unix/Linux exit code conventions with some application-specific additions.
    """
    SUCCESS = 0
    GENERAL_ERROR = 1
    MISUSE_OF_SHELL_BUILTIN = 2
    INVALID_USAGE = 64
    DESTINATION_ERROR = 73  # Data error
    DOWNLOAD_ERROR = 74     # Input/output error
    CONFIG_ERROR = 78       # Configuration error

def main():
    """
    Main entry point for the CLI application
    """
    try:
        # Use factory to create CLI app with dependencies
        app = Factory.create_cli_app()
        
        # Get command-line arguments
        cli_args = sys.argv[1:] if len(sys.argv) > 1 else None
        
        # Run the application
        app.run(cli_args)
        
        # Exit with success code
        sys.exit(ExitCode.SUCCESS)
    
    except CLIAppError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(ExitCode.GENERAL_ERROR)
    
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(ExitCode.GENERAL_ERROR)

if __name__ == '__main__':
    main()

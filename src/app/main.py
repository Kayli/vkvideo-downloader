import os
import sys
import yaml
import argparse
from typing import List, Dict, Optional, Union

# Import classes from other modules
from .extractor import Extractor
from .exporter import VideoLinkExporter, OUTPUT_YAML_FILE
from .logger import Logger
from .cli_app import CLIApp

if __name__ == '__main__':
    CLIApp().run()

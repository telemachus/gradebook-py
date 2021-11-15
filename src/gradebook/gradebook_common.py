"""Shared code for gradebook."""
import json
from pathlib import Path
import sys


def load_config(config_file):
    """Return JSON configuration file as Python dict object."""
    with open(config_file, mode="rt", encoding="utf-8") as config_handle:
        return json.load(config_handle)


def warn(msg, program_name=True):
    """Print a message to stderr and optionally add program’s name."""
    if program_name:
        msg = f"{Path(sys.argv[0]).name}: {msg}"
    print(msg, file=sys.stderr)


def die(msg, program_name=True):
    """Print a message to stderr and optionally add program’s name."""
    if program_name:
        msg = f"{Path(sys.argv[0]).name}: {msg}"
    sys.exit(msg)

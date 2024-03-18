"""Shared code for gradebook."""

import json
import sys
from pathlib import Path


def warn(msg, program_name=True):
    """Prints a message to stderr and optionally adds program’s name."""
    if program_name:
        msg = f"{Path(sys.argv[0]).name}: {msg}"
    print(msg, file=sys.stderr)


def die(msg, program_name=True):
    """Prints a message to stderr and optionally adds program’s name."""
    if program_name:
        msg = f"{Path(sys.argv[0]).name}: {msg}"
    sys.exit(msg)


def load_config(config_file):
    """Returns JSON configuration file as Python dict object."""
    with open(config_file, mode="rt", encoding="utf-8") as config_handle:
        return json.load(config_handle)


def load_config_or_die(config_file):
    """Returns configuration data or exits with system failure."""
    try:
        cfg = load_config(config_file)
    except (FileNotFoundError, TypeError):
        die(f"can't open {config_file.name}")
    except json.JSONDecodeError:
        die(f"bad json in {config_file.name}")

    return cfg

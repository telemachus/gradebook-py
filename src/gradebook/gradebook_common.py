"""Shared code for gradebook."""

import json
import sys
from pathlib import Path


def warn(msg, program_name=True):
    """Prints a message to stderr and optionally adds program's name."""
    if program_name:
        msg = f"{Path(sys.argv[0]).name}: {msg}"
    print(msg, file=sys.stderr)


def die(msg, program_name=True):
    """Prints a message to stderr and optionally adds program's name."""
    if program_name:
        msg = f"{Path(sys.argv[0]).name}: {msg}"
    sys.exit(msg)


def load_json(json_file):
    """Returns JSON file as Python dict object."""
    with open(json_file, mode="rt", encoding="utf-8") as json_handle:
        return json.load(json_handle)


def load_json_or_die(json_file):
    """Returns JSON data or exits with system failure."""
    try:
        data = load_json(json_file)
    except (FileNotFoundError, TypeError):
        die(f"cannot open {json_file.name}")
    except json.JSONDecodeError:
        die(f"bad JSON in {json_file.name}")

    return data

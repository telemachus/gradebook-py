"""usage: gradebook names [--last-first]

options:
    --last-first, -l        Show names in Last, First order
    --help, -h              Show this help screen

"""
from datetime import datetime
from pathlib import Path
import json
import re
from docopt import docopt
from gradebook.gradebook_common import load_config as gb_load_config
from gradebook.gradebook_common import die as gb_die

CONFIG_FILE = Path.cwd() / "class.json"


def compose_student_names(students, last_first=False):
    """Return a list of formatted student names.

    students: a dict of student information
    last_first: a boolean to switch how to order the names By default
    names appear as "First Last". But if last_first is true, then they
    are appear as "Last, First".

    Return value is a list of names in the desired format.
    """
    if last_first:
        return [f"{s['last_name']}, {s['first_name']}" for s in students.values()]

    return [f"{s['first_name']} {s['last_name']}" for s in students.values()]


def main(calc_args):
    """Start here."""
    flags = docopt(__doc__, argv=calc_args)
    last_first = flags["--last-first"]

    try:
        cfg = gb_load_config(CONFIG_FILE)
    except (FileNotFoundError, TypeError):
        gb_die(f"can't open {CONFIG_FILE.name}")
    except json.JSONDecodeError:
        gb_die(f"bad json in {CONFIG_FILE.name}")

    student_names = compose_student_names(cfg["students"], last_first)
    for s in student_names:
        print(s)

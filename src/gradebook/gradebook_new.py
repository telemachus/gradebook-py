"""usage: gradebook new --type TYPE --name NAME [--date DATE]

options:
    --type TYPE, -t TYPE    Specify assignment’s type (required)
    --name NAME, -n NAME    Specify assignment’s name (required)
    --date DATE, -d DATE    Specify assignment’s date (optional)
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
TODAY_YMD = datetime.today().strftime("%Y%m%d")


def validate_assignment_type(assignment_type, assignment_types):
    """Return assignment_type if it is a valid assignment type.

    assignment_type: string description of assignment type
    assignment_types: list of valid assignment types

    Raise ValueError if assignment_type is not in assignment_types.
    """
    if assignment_type not in assignment_types:
        raise ValueError()
    return assignment_type


def validate_assignment_name(assignment_name):
    """Return assignment_name if it contains only valid characters.

    assignment_name: string name of an assignment to validate.

    Raise ValueError if assignment_name contains anything other than
    upper- or lowercase letters, numbers, a period, - or _.
    """
    forbidden = re.compile("[^a-zA-Z0-9-_.]")
    fixed_name = forbidden.sub("", assignment_name)

    if assignment_name != fixed_name:
        raise ValueError()
    return assignment_name


def validate_assignment_date(date_string=TODAY_YMD):
    """Return date_string if it is a valid %Y%m%d date.

    date_string: string representation of a date to check

    datetime will raise ValueError if date_string does not match %Y%m%d
    format.
    """
    return datetime.strptime(date_string, "%Y%m%d").strftime("%Y%m%d")


def validate_file_name_unique(file_path):
    """Return file_path if it is unique.

    file_path: a pathlib object to test for uniqueness

    Raise ValueError if file_path already exists.
    """
    if file_path.exists():
        raise ValueError()
    return file_path


def make_assignment_grades(students):
    """Create a list of assignment grade entries from a dict of students.

    students: a dict of dicts with student information

    Returns a list of dicts. Each item in the list is a dict containing
    a student email and an initial grade of None.
    """
    assignment_grades = []
    for student_email in students.keys():
        assignment_grades.append({"email": student_email, "grade": None})
    sorted_assignment_grades = sorted(
        assignment_grades,
        key=lambda x: (
            students[x["email"]]["last_name"],
            students[x["email"]]["first_name"],
            x["email"],
        ),
    )
    return sorted_assignment_grades


def make_file_name(assignment_type, assignment_name, ymd):
    """Return gradebook filename as an absolute path."""
    file_name = f"{assignment_type}-{assignment_name}-{ymd}.gradebook"
    file_path = Path.cwd() / file_name
    return file_path


def build_gradebook(a_date, a_name, a_type, a_category, students):
    """Return full gradebook dict to be stored as JSON."""
    gradebook = {
        "assignment_date": a_date,
        "assignment_name": a_name,
        "assignment_type": a_type,
        "assignment_category": a_category,
        "assignment_grades": students,
    }
    return gradebook


def write_json(obj, file_path):
    """Write a Python object to a file as json."""
    with file_path.open(mode="wt", encoding="utf-8") as grades_file:
        json.dump(obj, grades_file, indent=4)


def main(calc_args):
    """Start here."""
    arguments = docopt(__doc__, argv=calc_args)
    assignment_type = arguments["--type"]
    assignment_name = arguments["--name"]
    assignment_date = arguments["--date"]

    try:
        cfg = gb_load_config(CONFIG_FILE)
    except (FileNotFoundError, TypeError):
        gb_die(f"can't open {CONFIG_FILE.name}")
    except json.JSONDecodeError:
        gb_die(f"bad json in {CONFIG_FILE.name}")

    assignment_types = cfg["types_to_categories"].keys()
    try:
        validate_assignment_type(assignment_type, assignment_types)
    except ValueError:
        msg = f"{assignment_type} is not a valid type: "
        msg += "update class.json or pick a valid type.\n"
        msg += f"Here are the valid types: {', '.join(assignment_types)}."
        gb_die(msg)

    try:
        validate_assignment_name(assignment_name)
    except ValueError:
        msg = f"“{assignment_name}” is not a valid name: "
        msg += "use only a-z, A-Z, 0-9, - and _ in the name."
        gb_die(msg)

    try:
        validate_assignment_date(assignment_date)
    except ValueError:
        gb_die(f"{assignment_date} is not a valid date")

    file_name = make_file_name(assignment_type, assignment_name, assignment_date)
    try:
        validate_file_name_unique(file_name)
    except ValueError:
        gb_die(f"{file_name} already exists: use another name")

    assignment_grades = make_assignment_grades(cfg["students"])
    gradebook = build_gradebook(
        assignment_date,
        assignment_name,
        assignment_type,
        cfg["types_to_categories"][assignment_type],
        assignment_grades,
    )

    try:
        write_json(gradebook, file_name)
    except OSError:
        gb_die(f"failed to write json to {file_name}")

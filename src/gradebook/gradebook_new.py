"""usage: gradebook new --type TYPE --name NAME [--date DATE]

options:
    --type TYPE, -t TYPE    Specify assignment's type (required)
    --name NAME, -n NAME    Specify assignment's name (required)
    --date DATE, -d DATE    Specify assignment's date (optional)
    --help, -h              Show this help screen

"""

import json
import re
from datetime import datetime
from pathlib import Path

from docopt import docopt

from gradebook.gradebook_common import die as gb_die
from gradebook.gradebook_common import load_json_or_die as gb_load_json_or_die

CONFIG_FILE = Path.cwd() / "class.json"


def normalize_date(date_argument):
    if date_argument is None:
        return datetime.today().strftime("%Y%m%d")

    return date_argument


def validate_assignment_type(assignment_type, assignment_types):
    """Validates a given assignment type.

    Args:
        assignment_type:
            String representing an assignment type.
        assignment_types:
            List of recognized assignment types.

    Raises:
        ValueError: When assignment_type is not in assignment_types.
    """
    if assignment_type not in assignment_types:
        raise ValueError()
    return assignment_type


def validate_assignment_type_or_die(assignment_type, assignment_types):
    """Die if assignment_type is not in assignment_types."""
    try:
        validate_assignment_type(assignment_type, assignment_types)
    except ValueError:
        msg = f"{assignment_type} is not a valid type: "
        msg += "update class.json or pick a valid type.\n"
        msg += f"Here are the valid types: {", ".join(assignment_types)}."
        gb_die(msg)


def validate_assignment_name(assignment_name):
    """Validates a given assignment name.

    Args:
        assignment_name:
            String representing an assignment name.

    Raises:
        ValueError: Names must be letters, numbers, or some punctuation.
    """
    forbidden = re.compile("[^a-zA-Z0-9-_.]")
    fixed_name = forbidden.sub("", assignment_name)

    if assignment_name != fixed_name:
        raise ValueError()
    return assignment_name


def validate_assignment_name_or_die(assignment_name):
    """Dies if assignment_name has invalid characters."""
    try:
        validate_assignment_name(assignment_name)
    except ValueError:
        msg = f"“{assignment_name}” is not a valid name: "
        msg += "use only a-z, A-Z, 0-9, - and _ in the name."
        gb_die(msg)


def validate_assignment_date(date_string):
    """Validates a given date.

    Args:
        date_string:
            String representation of a date.

    Raises:
        ValueError: When date_string does not match %Y%m%d format.
    """
    return datetime.strptime(date_string, "%Y%m%d").strftime("%Y%m%d")


def validate_assignment_date_or_die(date_string):
    """Dies if date_string is not a valid YMD date."""
    if date_string is None:
        date_string = datetime.today().strftime("%Y%m%d")
    try:
        validate_assignment_date(date_string)
    except ValueError:
        gb_die(f"{date_string} is not a valid date")


def make_assignment_grades(students):
    """Creates a list of assignment grade entries from a dict of students.

    Args:
        students:
            A dict of dicts with student information.

    Returns:
        A sorted list of dicts. Each item in the list is a dict containing
        a student email and an initial grade of None. The list is sorted by
        last name, and duplicate last names are sorted by first name. In a
        case where two students have the identical name, they are sorted by
        emails, which must be unique.
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
    """Creates a name for the new gradebook file."""
    file_name = f"{assignment_type}-{assignment_name}-{ymd}.gradebook"
    file_name = Path.cwd() / file_name
    return file_name


def build_gradebook(a_date, a_name, a_type, a_category, students):
    """Returns full gradebook dict to be stored as JSON."""
    gradebook = {
        "assignment_date": a_date,
        "assignment_name": a_name,
        "assignment_type": a_type,
        "assignment_category": a_category,
        "assignment_grades": students,
    }
    return gradebook


def write_json(obj, file_path):
    """Writes a Python object to a file as json."""
    with file_path.open(mode="xt", encoding="utf-8") as grades_file:
        json.dump(obj, grades_file, indent=4)


def main(calc_args):
    """Starts here."""
    arguments = docopt(__doc__, argv=calc_args)
    assignment_type = arguments["--type"]
    assignment_name = arguments["--name"]
    assignment_date = normalize_date(arguments["--date"])

    cfg = gb_load_json_or_die(CONFIG_FILE)

    assignment_types = cfg["categories_by_assignment_type"].keys()
    validate_assignment_type_or_die(assignment_type, assignment_types)
    validate_assignment_name_or_die(assignment_name)
    validate_assignment_date_or_die(arguments["--date"])
    file_name = make_file_name(assignment_type, assignment_name, assignment_date)

    assignment_grades = make_assignment_grades(cfg["students_by_email"])
    gradebook = build_gradebook(
        assignment_date,
        assignment_name,
        assignment_type,
        cfg["categories_by_assignment_type"][assignment_type],
        assignment_grades,
    )

    try:
        write_json(gradebook, file_name)
    except OSError:
        gb_die(f"failed to write JSON to {file_name}")

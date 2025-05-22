"""usage:
    gradebook calculate [--semester N|--quarter N]
    gradebook calc [--semester N|--quarter N]

options:
    --semester N, -s N          Calculate grades for semester N
    --quarter N, -q N           Calculate grades for quarter N
    --help, -h                  Show this message

"""

import json
import sys
from pathlib import Path

from docopt import docopt

from gradebook.gradebook_common import load_json_or_die as gb_load_json_or_die
from gradebook.gradebook_student import Student

CONFIG_FILE = Path.cwd() / "class.json"


def get_term_filter(quarter_or_semester, terms):
    """Returns a dict with start and end of term or raise ValueError."""
    try:
        return terms[quarter_or_semester]
    except KeyError as key_error:
        raise ValueError() from key_error


def is_in_term(assignment_date, term):
    """Tests whether an assignment date falls within a specified term."""
    return term["start"] <= assignment_date <= term["end"]


def load_students(students_dict, categories):
    """Creates and returns a dict of Student objects."""
    student_objs = {}
    for student in students_dict.keys():
        email = student
        fname = students_dict[student]["first_name"]
        lname = students_dict[student]["last_name"]
        student_objs[email] = Student(fname, lname, email, categories)

    return student_objs


def extract_date(file_path):
    """Extracts the date from a file path."""
    return file_path.stem[-8:]


def grade_data_generator(path, date_filter=None):
    """Yields data from grade files."""
    for file_path in Path(path).glob("*.gradebook"):
        if date_filter:
            date = extract_date(file_path)
            if not is_in_term(date, date_filter):
                continue
        yield gb_load_json_or_die(file_path)


def load_grades(student_objs, path, data_filter=None):
    """Loads all grades from gradebook files."""
    for grade_data in grade_data_generator(path, data_filter):
        assignment_category = grade_data["assignment_category"]
        for student in grade_data["assignment_grades"]:
            if student["grade"] is not None:
                try:
                    student_objs[student["email"]].add_grade(
                        student["grade"], assignment_category
                    )
                except KeyError:
                    # TODO: I should print something to stderr here.
                    pass


def display_grades(students, categories_pretty, weights):
    """Sorts the students list and displays grades."""
    for student in sorted(students.values(), key=lambda s: s.last_name):
        print(f"{student.first_name} {student.last_name}")
        print(f"\tOverall grade: {student.total_average(weights)}")

        for category, category_pretty in categories_pretty.items():
            print(f"\t{category_pretty}: {student.average(category)}")


def main(calc_args):
    """Starts here."""
    arguments = docopt(__doc__, argv=calc_args)
    quarter = arguments["--quarter"]
    semester = arguments["--semester"]

    cfg = gb_load_json_or_die(CONFIG_FILE)

    students = load_students(cfg["students"], cfg["categories"])

    if quarter is not None:
        try:
            term_filter = get_term_filter("q" + quarter, cfg["terms"])
            load_grades(students, Path.cwd(), term_filter)
        except ValueError:
            sys.exit(
                f"{quarter} is not a valid quarter. "
                f"Valid quarters are {{1, 2, 3, 4}}."
            )
    elif semester is not None:
        try:
            term_filter = get_term_filter("s" + semester, cfg["terms"])
            load_grades(students, Path.cwd(), term_filter)
        except ValueError:
            sys.exit(
                f"{semester} is not a valid semester. Valid semesters are {{1, 2}}."
            )
    else:
        load_grades(students, Path.cwd())

    display_grades(students, cfg["categories_pretty"], cfg["category_weights"])

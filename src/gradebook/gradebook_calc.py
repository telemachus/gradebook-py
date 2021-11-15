"""usage:
    gradebook calc|calculate    [--semester N|--quarter N]

options:
    --semester N, -s N          Calculate grades for semester N
    --quarter N, -q N           Calculate grades for quarter N
    --help, -h                  Show this message

"""
import json
from pathlib import Path
from sys import exit
from docopt import docopt
from gradebook.gradebook_common import load_config as gb_load_config
from gradebook.gradebook_common import die as gb_die
from gradebook.gradebook_student import Student

CONFIG_FILE = Path.cwd() / "class.json"


def get_term_filter(quarter_or_semester, terms):
    """Return a dict with start and end of term or raise ValueError."""
    try:
        return terms[quarter_or_semester]
    except KeyError:
        raise ValueError()


def is_in_term(assignment_date, term):
    """Test whether an assignment date falls within a specified term."""
    return term["start"] <= assignment_date <= term["end"]


def load_students(students_dict, categories):
    """Create and return a dict of Student objects."""
    student_objs = {}
    for student in students_dict.keys():
        email = student
        fname = students_dict[student]["first_name"]
        lname = students_dict[student]["last_name"]
        student_objs[email] = Student(fname, lname, email, categories)

    return student_objs


def extract_date(file_path):
    """Extract the date from a file path."""
    return file_path.stem[-8:]


def grade_data_generator(date_filter=None):
    """Yield data from .gradebook files."""
    for file_path in Path(".").glob("*.gradebook"):
        if date_filter:
            date = extract_date(file_path)
            if not is_in_term(date, date_filter):
                continue
        with open(file_path, mode="rt", encoding="utf-8") as file_handle:
            yield json.load(file_handle)


def load_grades(student_objs, data_filter=None):
    """Load all grades."""
    for grade_data in grade_data_generator(data_filter):
        assignment_category = grade_data["assignment_category"]
        students = grade_data["assignment_grades"]
        for student in students.keys():
            grade = students[student]["grade"]
            if grade:
                student_objs[student].add_grade(grade, assignment_category)


def display_grades(students, categories_pretty, weights):
    """Sort the students list and display grades."""
    for student in sorted(students.values(), key=lambda s: s.last_name):
        print(f"{student.first_name} {student.last_name}")

        print(f"\tOverall grade: {student.total_average(weights)}")
        for category, category_pretty in categories_pretty.items():
            print(f"\t{category_pretty}: {student.average(category)}")


def main(calc_args):
    """Start here."""
    arguments = docopt(__doc__, argv=calc_args)
    quarter = arguments["--quarter"]
    semester = arguments["--semester"]

    try:
        cfg = gb_load_config(CONFIG_FILE)
    except (FileNotFoundError, TypeError):
        gb_die(f"can't open {CONFIG_FILE.name}")
    except json.JSONDecodeError:
        gb_die(f"bad json in {CONFIG_FILE.name}")

    students = load_students(cfg["students"], cfg["categories"])

    if quarter is not None:
        term_filter = get_term_filter("q" + quarter, cfg["terms"])
        load_grades(students, term_filter)
    elif semester is not None:
        term_filter = get_term_filter("s" + semester, cfg["terms"])
        load_grades(students, term_filter)
    else:
        load_grades(students)

    display_grades(students, cfg["categories_pretty"], cfg["category_weights"])

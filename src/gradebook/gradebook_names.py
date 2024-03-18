"""usage: gradebook names [--last-first]

options:
    --last-first, -l        Show names in Last, First order
    --help, -h              Show this help screen

"""

from pathlib import Path

from docopt import docopt

from gradebook.gradebook_common import load_config_or_die as gb_load_config_or_die

CONFIG_FILE = Path.cwd() / "class.json"


def compose_student_names(students, last_first=False):
    """Returns a list of formatted student names.

    Args:
        students:
            A dict of student information.
        last_first:
            A boolean to control how the names appear. By default names
            appear as "First Last". But if last_first is true, then they
            appear as "Last, First".

    Returns:
        A list of names in the desired format.
    """
    if last_first:
        return [f"{s['last_name']}, {s['first_name']}" for s in students.values()]

    return [f"{s['first_name']} {s['last_name']}" for s in students.values()]


def main(calc_args):
    """Starts here."""
    flags = docopt(__doc__, argv=calc_args)
    last_first = flags["--last-first"]

    cfg = gb_load_config_or_die(CONFIG_FILE)

    student_names = compose_student_names(cfg["students"], last_first)
    for student in student_names:
        print(student)

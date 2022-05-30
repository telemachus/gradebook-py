"""usage: gradebook [--version] [--help] <command> [<args>...]

options:
    --help, -h          Show this message
    --version, -v       Show version

The following commands are available:
    calc(ulate)         Calculate grades for quarter, semester, or year
    names               Show names for the current class
    new                 Generate a gradebook file for a specified assignment

See 'gradebook <command> --help for information about specific commands.

"""
from docopt import docopt
from gradebook.gradebook_calc import main as gbcalc_main
from gradebook.gradebook_common import warn as gb_warn, die as gb_die
from gradebook.gradebook_names import main as gbnames_main
from gradebook.gradebook_new import main as gbnew_main


def main():
    """Parses command line and hands off to subcommands."""
    args = docopt(__doc__, version="gradebook v0.5.0", options_first=True)
    cmd = args["<command>"]
    cmd_args = [cmd] + args["<args>"]
    if cmd == "new":
        gbnew_main(cmd_args)
    elif cmd in ["calc", "calculate"]:
        gbcalc_main(cmd_args)
    elif cmd == "names":
        gbnames_main(cmd_args)
    else:
        gb_warn(f"invalid command -- {cmd}")
        gb_warn(__doc__[:-2], program_name=False)
        gb_die(2, program_name=False)


if __name__ == "__main__":
    main()

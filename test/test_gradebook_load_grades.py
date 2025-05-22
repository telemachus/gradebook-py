"""Tests load_grades from gradebook_calc."""

from pathlib import Path

from gradebook import gradebook_calc as gbc
from gradebook import gradebook_student as gbs


def test_load_grades_null_vs_zero():
    john = gbs.Student("John", "Doe", "john.doe@school.edu", ["major"])
    jane = gbs.Student("Jane", "Doe", "jane.doe@school.edu", ["major"])
    student_objs = {john.email: john, jane.email: jane}
    gbc.load_grades(student_objs, Path.cwd() / "test/data")

    assert john.has_grades("major") == True
    assert jane.has_grades("major") == False


def test_load_grades_catches_key_error():
    student_objs = {}
    gbc.load_grades(student_objs, Path.cwd() / "test/data")

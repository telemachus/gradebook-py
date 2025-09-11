"""Tests gradebook_student."""

import pytest

from gradebook import gradebook_student as gbs


@pytest.mark.parametrize(
    "fname, lname, email",
    [
        ("Michael", "Frede", "mfrede@school.edu"),
        ("Gisela", "Striker", "gstriker@school.edu"),
        ("Julia", "Annas", "jannas@school.edu"),
    ],
)
def test_student_initialization(fname, lname, email):
    category = "major"
    categories = {category: True}
    random_student = gbs.Student(fname, lname, email, categories)
    assert fname == random_student.first_name
    assert lname == random_student.last_name
    assert email == random_student.email


def test_add_grade():
    fname = "Michael"
    lname = "Frede"
    email = "mfrede@school.edu"
    category = "major"
    assignment_types = [category]
    grade = 89.9
    michael_frede = gbs.Student(fname, lname, email, assignment_types)
    michael_frede.add_grade(grade, category)
    # pylint: disable=protected-access
    assert grade == michael_frede._assignment_types[category][0]


def test_average():
    fname = "Michael"
    lname = "Frede"
    email = "mfrede@school.edu"
    category = "major"
    assignment_types = [category]
    michael_frede = gbs.Student(fname, lname, email, assignment_types)
    assert "No results" == michael_frede.average(category)

    grades = [85, 90, 95]
    for grade in grades:
        michael_frede.add_grade(grade, category)
    assert 90 == michael_frede.average(category)


def test_total_average():
    fname = "Michael"
    lname = "Frede"
    email = "mfrede@school.edu"
    assignment_types = ["major", "minor", "cp"]
    weights_by_assignment_type = {"major": 50, "minor": 30, "cp": 20}
    michael_frede = gbs.Student(fname, lname, email, assignment_types)
    assert "No results" == michael_frede.total_average(weights_by_assignment_type)

    grades = [90, 90, 90]
    for grade, assignment_type in zip(grades, assignment_types):
        michael_frede.add_grade(grade, assignment_type)
    assert 90 == michael_frede.total_average(weights_by_assignment_type)

    grades = [(94, "major"), (82, "minor"), (75, "cp")]
    for grade, assignment_type in grades:
        michael_frede.add_grade(grade, assignment_type)
    assert 88 == michael_frede.total_average(weights_by_assignment_type)

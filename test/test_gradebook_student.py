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
    assert random_student.first_name == fname
    assert random_student.last_name == lname
    assert random_student.email == email
    assert random_student._categories[category] == []


def test_add_grade():
    fname = "Michael"
    lname = "Frede"
    email = "mfrede@school.edu"
    category = "major"
    categories = {category: True}
    grade = 89.9
    michael_frede = gbs.Student(fname, lname, email, categories)
    michael_frede.add_grade(grade, category)
    assert michael_frede._categories[category][0] == grade


def test_average():
    fname = "Michael"
    lname = "Frede"
    email = "mfrede@school.edu"
    category = "major"
    categories = {category: True}
    michael_frede = gbs.Student(fname, lname, email, categories)
    assert michael_frede.average(category) == "No results"

    grades = [85, 90, 95]
    for grade in grades:
        michael_frede.add_grade(grade, category)
    assert michael_frede.average(category) == 90


def test_total_average():
    fname = "Michael"
    lname = "Frede"
    email = "mfrede@school.edu"
    categories = {"major": True, "minor": True, "cp": True}
    weights = {"major": 50, "minor": 30, "cp": 20}
    michael_frede = gbs.Student(fname, lname, email, categories)
    assert michael_frede.total_average(weights) == "No results"

    grades = [90, 90, 90]
    for grade, category in zip(grades, categories.keys()):
        michael_frede.add_grade(grade, category)
    assert michael_frede.total_average(weights) == 90

    grades = [(94, "major"), (82, "minor"), (75, "cp")]
    for grade, category in grades:
        michael_frede.add_grade(grade, category)
    assert michael_frede.total_average(weights) == 88

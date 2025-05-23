"""Tests load_grades from gradebook_calc."""

from pathlib import Path

import pytest

from gradebook import gradebook_calc as gbc
from gradebook import gradebook_student as gbs


# pylint: disable=redefined-outer-name
@pytest.fixture
def john():
    return gbs.Student("John", "Doe", "john.doe@school.edu", ["major"])


@pytest.fixture
def jane():
    return gbs.Student("Jane", "Doe", "jane.doe@school.edu", ["major"])


@pytest.fixture
def student_pair(john, jane):
    return {john.email: john, jane.email: jane}


def test_load_grades_null_vs_zero(student_pair, john, jane):
    gbc.load_grades(student_pair, Path.cwd() / "test/data")

    assert john.has_grades("major") is True
    assert jane.has_grades("major") is False


def test_load_grades_catches_key_error():
    student_objs = {}
    gbc.load_grades(student_objs, Path.cwd() / "test/data")

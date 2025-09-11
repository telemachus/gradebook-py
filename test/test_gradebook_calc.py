"""Tests gradebook_calc."""

from pathlib import Path

import pytest

from gradebook import gradebook_calc as gbc
from gradebook import gradebook_student as gbs


@pytest.mark.parametrize("term", ["q1", "q2", "q3", "q4", "s1", "s2"])
def test_get_term_filter(term):
    terms = {"q1": "q1", "q2": "q2", "q3": "q3", "q4": "q4", "s1": "s1", "s2": "s2"}
    assert term == gbc.get_term_filter(term, terms)


@pytest.mark.parametrize("term", ["q5", "2", "s3", "r4"])
def test_get_term_filter_exception(term):
    terms = {}
    with pytest.raises(ValueError):
        gbc.get_term_filter(term, terms)


@pytest.mark.parametrize(
    "assignment_date,expected",
    [
        ("20200907", False),
        ("20200908", True),
        ("20201001", True),
        ("20201106", True),
        ("20201107", False),
    ],
)
def test_is_in_term(assignment_date, expected):
    term = {"start": "20200908", "end": "20201106"}
    assert expected == gbc.is_in_term(assignment_date, term)


def test_load_students():
    peter = gbs.Student(
        "Peter", "Aronoff", "peter@school.edu", ["major", "minor", "cp"]
    )
    expected_dict = {"peter@school.edu": peter}
    actual_dict = gbc.load_students(
        {
            "peter@school.edu": {"first_name": "Peter", "last_name": "Aronoff"},
        },
        ["major", "minor", "cp"],
    )
    assert expected_dict.keys() == actual_dict.keys()
    assert (
        expected_dict["peter@school.edu"].first_name
        == actual_dict["peter@school.edu"].first_name
    )
    assert (
        expected_dict["peter@school.edu"].last_name
        == actual_dict["peter@school.edu"].last_name
    )
    assert (
        # pylint: disable=protected-access
        expected_dict["peter@school.edu"]._assignment_types
        == actual_dict["peter@school.edu"]._assignment_types
    )


@pytest.mark.parametrize(
    "file_path,extracted_date",
    [
        ("essay-foo-20200901.gradebook", "20200901"),
        ("quiz-bar-20211115.gradebook", "20211115"),
        ("cp-buzz-20220101.gradebook", "20220101"),
        ("hw-ovid-2.10-12-19991212.gradebook", "19991212"),
    ],
)
def test_extract_date(file_path, extracted_date):
    file_path = Path.cwd() / file_path
    assert extracted_date == gbc.extract_date(file_path)

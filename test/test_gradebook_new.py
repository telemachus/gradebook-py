from pathlib import Path
import pytest
from datetime import datetime
from gradebook import gradebook_new as gbn


@pytest.mark.parametrize("date", ["20000101", "19680809"])
def test_normalize_date_with_date_given(date):
    assert date == gbn.normalize_date(date)


def test_normalize_date_when_date_none():
    ymd = datetime.today().strftime("%Y%m%d")
    assert ymd == gbn.normalize_date(None)


@pytest.mark.parametrize("ast_type", ["quiz", "test", "cp"])
def test_validate_assignment_type(ast_type):
    ast_types = ["cp", "quiz", "test"]
    assert ast_type == gbn.validate_assignment_type(ast_type, ast_types)


@pytest.mark.parametrize("ast_type", ["quest", "essay", "paper"])
def test_validate_assignment_type_exception(ast_type):
    ast_types = ["cp", "quiz", "test"]
    with pytest.raises(ValueError):
        gbn.validate_assignment_type(ast_type, ast_types)


def test_validate_assignment_name():
    ast_name = "vergil-2.101-123"
    assert ast_name == gbn.validate_assignment_name(ast_name)


def test_validate_assignment_name_exception():
    ast_name = "vergil 2.101-123"
    with pytest.raises(ValueError):
        gbn.validate_assignment_name(ast_name)


def test_validate_assignment_date():
    ymd = "19970727"
    assert ymd == gbn.validate_assignment_date(ymd)


def test_validate_assignment_date_exception():
    ymd = "19970747"
    with pytest.raises(ValueError):
        gbn.validate_assignment_date(ymd)


def test_validate_file_name_unique():
    file_name = Path("quiz-vergil-2.101-123-19970727.gradebook")
    assert file_name == gbn.validate_file_name_unique(file_name)


def test_validate_file_name_unique_exception(tmpdir):
    file_path = tmpdir.join("quiz-vergil-2.101-123-19970727.gradebook")
    file_path.write("Can you hear me now?")
    with pytest.raises(ValueError):
        gbn.validate_file_name_unique(file_path)


def test_make_assignment_grades():
    students = {
        "mfrede02@school.edu": {"first_name": "Michael", "last_name": "Frede"},
        "gstriker@school.edu": {"first_name": "Gisela", "last_name": "Striker"},
        "mfrede01@school.edu": {"first_name": "Michael", "last_name": "Frede"},
    }
    expected_assignment_grades = [
        {
            "email": "mfrede01@school.edu",
            "grade": None,
        },
        {
            "email": "mfrede02@school.edu",
            "grade": None,
        },
        {
            "email": "gstriker@school.edu",
            "grade": None,
        },
    ]
    assert expected_assignment_grades == gbn.make_assignment_grades(students)


def test_make_file_name():
    expected_file_name = Path.cwd() / "quiz-vergil-2.101-123-19970727.gradebook"
    assert expected_file_name == gbn.make_file_name(
        "quiz", "vergil-2.101-123", "19970727"
    )


def test_build_gradebook():
    # {{{ List of dicts of students
    students = [
        {
            "email": "mfrede@school.edu",
            "grade": None,
        },
        {
            "email": "gstriker@school.edu",
            "grade": None,
        },
    ]
    gradebook_after = {
        "assignment_date": "19970727",
        "assignment_name": "vergil-2.101-110",
        "assignment_type": "quiz",
        "assignment_category": "minor",
        "assignment_grades": students,
    }
    # }}}
    assert gradebook_after == gbn.build_gradebook(
        "19970727", "vergil-2.101-110", "quiz", "minor", students
    )


def test_write_json(tmp_path):
    obj = {"class": None}
    file_path = tmp_path / "quiz-vergil-2.101-123-19970727.gradebook"
    gbn.write_json(obj, file_path)
    assert file_path.exists()

"""Test src/gradebook/gradebook_new."""
from pathlib import Path
import pytest
from gradebook import gradebook_new as gbn


@pytest.mark.parametrize("ast_type", ["quiz", "test", "cp"])
def test_validate_assignment_type(ast_type):
    ast_types = ["cp", "quiz", "test"]
    assert gbn.validate_assignment_type(ast_type, ast_types) == ast_type


@pytest.mark.parametrize("ast_type", ["quest", "essay", "paper"])
def test_validate_assignment_type_exception(ast_type):
    ast_types = ["cp", "quiz", "test"]
    with pytest.raises(ValueError):
        gbn.validate_assignment_type(ast_type, ast_types)


def test_validate_assignment_name():
    ast_name = "vergil-2.101-123"
    returned_name = gbn.validate_assignment_name(ast_name)
    assert returned_name == ast_name


def test_validate_assignment_name_exception():
    ast_name = "vergil 2.101-123"
    with pytest.raises(ValueError):
        gbn.validate_assignment_name(ast_name)


def test_validate_assignment_date():
    ymd = "19970727"
    returned_ymd = gbn.validate_assignment_date(ymd)
    assert returned_ymd == ymd


def test_validate_assignment_date_exception():
    ymd = "19970747"
    with pytest.raises(ValueError):
        gbn.validate_assignment_date(ymd)


def test_validate_file_name_unique():
    file_path = Path("quiz-vergil-2.101-123-19970727.gradebook")
    returned_file_path = gbn.validate_file_name_unique(file_path)
    assert returned_file_path == file_path


def test_validate_file_name_unique_exception(tmpdir):
    file_path = tmpdir.join("quiz-vergil-2.101-123-19970727.gradebook")
    file_path.write("Can you hear me now?")
    with pytest.raises(ValueError):
        gbn.validate_file_name_unique(file_path)


def test_update_students():
    # {{{ Lists of dicts of students with and without grade keys
    students_before = {
        "gstriker@school.edu": {
            "first_name": "Gisela",
            "last_name": "Striker"
        },
        "mfrede@school.edu": {
            "first_name": "Michael",
            "last_name": "Frede"
        },
    }
    students_after = {
        "gstriker@school.edu": {
            "first_name": "Gisela",
            "last_name": "Striker",
            "grade": None,
        },
        "mfrede@school.edu": {
            "first_name": "Michael",
            "last_name": "Frede",
            "grade": None,
        },
    }
    # }}}
    gbn.update_students(students_before)
    assert students_before == students_after


def test_make_file_name():
    quiz_file_path = Path.cwd() / "quiz-vergil-2.101-123-19970727.gradebook"
    other_file_path = gbn.make_file_name("quiz", "vergil-2.101-123", 19970727)
    assert quiz_file_path == other_file_path


def test_build_gradebook():
    # {{{ List of dicts of students
    students = [
        {
            "first_name": "Gisela",
            "last_name": "Striker",
            "email": "gstriker@school.edu",
            "grade": None,
        },
        {
            "first_name": "Michael",
            "last_name": "Frede",
            "email": "mfrede@school.edu",
            "grade": None,
        },
    ]
    gradebook_after = {
        "assignment_date": 19970727,
        "assignment_name": "vergil-2.101-110",
        "assignment_type": "quiz",
        "assignment_category": "minor",
        "assignment_grades": students,
    }
    # }}}
    test_gradebook = gbn.build_gradebook(
        19970727, "vergil-2.101-110", "quiz", "minor", students
    )
    assert test_gradebook == gradebook_after


def test_write_json(tmp_path):
    obj = {"class": None}
    file_path = tmp_path / "quiz-vergil-2.101-123-19970727.gradebook"
    gbn.write_json(obj, file_path)
    assert file_path.exists()

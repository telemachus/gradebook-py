"""Test src/gradebook/gradebook_new."""
from gradebook import gradebook_names as gbn


def test_student_names_lastfirst_false():
    students_dict = {
        "gstriker@school.edu": {"first_name": "Gisela", "last_name": "Striker"},
        "mfrede@school.edu": {"first_name": "Michael", "last_name": "Frede"},
    }
    students_list = ["Gisela Striker", "Michael Frede"]
    students = gbn.compose_student_names(students_dict)
    assert students == students_list


def test_student_names_lastfirst_true():
    students_dict = {
        "gstriker@school.edu": {"first_name": "Gisela", "last_name": "Striker"},
        "mfrede@school.edu": {"first_name": "Michael", "last_name": "Frede"},
    }
    students_list = ["Striker, Gisela", "Frede, Michael"]
    students = gbn.compose_student_names(students_dict, True)
    assert students == students_list

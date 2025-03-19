"""Tests gradebook_common."""

import sys

from pytest import raises

from gradebook import gradebook_common as gbc


def test_warn_no_program_name(capsys):
    msg = "bad input!"
    msg_err = msg + "\n"
    gbc.warn(msg, program_name=False)
    assert msg_err == capsys.readouterr().err


def test_warn_with_program_name(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["gradebook"])
    msg = "bad input!"
    msg_err = "gradebook: " + msg + "\n"
    gbc.warn(msg)
    assert msg_err == capsys.readouterr().err


def test_die_no_program_name(mocker):
    mocker.patch("sys.exit")
    msg = "bad input!"
    gbc.die(msg, program_name=False)
    sys.exit.assert_called_once_with(msg)


def test_die_with_program_name(mocker):
    mocker.patch("sys.argv", ["gradebook"])
    mocker.patch("sys.exit")
    msg = "bad input!"
    msg_err = "gradebook: " + msg
    gbc.die(msg)
    sys.exit.assert_called_once_with(msg_err)


# {{{ Python dict fixture to test JSON loading
dummy_dict = {
    "name": "Ancient Philosophy Survey",
    "terms": {
        "q1": {"start": "20200908", "end": "20201106"},
        "q2": {"start": "20201109", "end": "20210115"},
        "q3": {"start": "20200901", "end": "20201101"},
        "q4": {"start": "20200901", "end": "20201101"},
        "s1": {"start": "20200901", "end": "20201101"},
        "s2": {"start": "20200901", "end": "20201101"},
    },
    "categories": ["major", "minor", "cp"],
    "categories_pretty": {
        "major": "Major assessments",
        "minor": "Daily work and quizzes",
        "cp": "Class participation",
    },
    "category_weights": {"major": 50, "minor": 30, "cp": 20},
    "types_to_categories": {
        "test": "major",
        "project": "major",
        "essay": "major",
        "quiz": "minor",
        "hw": "minor",
        "cp": "cp",
    },
    "students": {
        "gstriker@school.edu": {"first_name": "Gisela", "last_name": "Striker"},
        "mfrede@school.edu": {"first_name": "Michael", "last_name": "Frede"},
        "jannas@school.edu": {"first_name": "Julia", "last_name": "Annas"},
        "agomezlobo@school.edu": {"first_name": "Alfonso", "last_name": "Gómez-Lobo"},
        "gfine@school.edu": {"first_name": "Gail", "last_name": "Fine"},
    },
}
# }}}


def test_load_json(shared_datadir):
    json_file = "class.json"
    assert dummy_dict == gbc.load_json(shared_datadir / json_file)


def test_load_json_or_die(shared_datadir):
    bad_json = "bad.json"
    nosuch_json = "nosuch.json"

    with raises(SystemExit) as e:
        gbc.load_json_or_die(shared_datadir / bad_json)

    with raises(SystemExit) as e:
        gbc.load_json_or_die(shared_datadir / nosuch_json)

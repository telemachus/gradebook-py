"""Checks most basic test setup."""

try:
    import gradebook  # noqa # pylint: disable=unused-import
except ModuleNotFoundError:
    print("`PYTHONPATH=src pytest` or `export PYTHONPATH=src && pytest`")
    raise


def test_pytest_setup():
    assert True

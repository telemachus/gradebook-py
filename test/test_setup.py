"""Most basic testing of my setup."""
try:
    import gradebook
except ModuleNotFoundError:
    print("`PYTHONPATH=src pytest` or `export PYTHONPATH=src && pytest`")
    raise


def test_pytest_setup():
    assert True

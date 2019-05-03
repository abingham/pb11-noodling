import pytest


def pytest_addoption(parser):
    """This adds the '--ex <exercise>' command-line option to pytest.
    """
    parser.addoption("--ex", action="store",
                     help="The exercise to test.")


def pytest_collection_modifyitems(config, items):
    """This looks for `for_exercise` markers on tests and skips tests which don't
    match the current exercise.

    """
    ex = config.getoption("--ex")
    ex = (int(ex[:-1]), ex[-1])

    skip_ex_pred = pytest.mark.skip(
        reason='not applicable to exercise {}'.format(ex))

    for item in items:
        try:
            fex = item.keywords['for_exercise']
            for pred in fex.args:
                if not pred(ex):
                    item.add_marker(skip_ex_pred)
        except KeyError:
            pass

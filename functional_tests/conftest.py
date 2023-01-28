import pytest


@pytest.fixture(scope="session")
def django_db_setup():
    pass


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests():
    pass


@pytest.fixture(autouse=True)
def enable_db_access(db):
    pass

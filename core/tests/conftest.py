import pytest
from digitalhub_core.entities.projects.crud import delete_project, get_or_create_project


@pytest.fixture
def api_base():
    return "/api/v1"


@pytest.fixture
def api_context():
    return "/api/v1/-"


@pytest.fixture(scope="session")
def project():
    yield get_or_create_project(name="test", local=True)
    delete_project(name="test")

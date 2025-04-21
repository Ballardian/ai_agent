import tempfile
import shutil
import pytest


from src.backend.database.client.chroma_client import ChromaClient
from tests.mock_data import get_mock_data


@pytest.fixture(scope="session", autouse=True)
def temp_db_dir():
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Cleanup after test session
    shutil.rmtree(temp_dir)


@pytest.fixture
def chroma_client(temp_db_dir):
    return ChromaClient(collection_name="test_collection", path=temp_db_dir)


def test_add_content(chroma_client):
    content_list = get_mock_data()

    for content in content_list.values():
        chroma_client.add_content(content)

    assert chroma_client.collection.count() == 4


def test_fetch_content(chroma_client):
    content_list = get_mock_data()
    results = chroma_client.fetch_content(
        query_texts=["I want a english book"], where={"subject": "english"}
    )
    ids = results["ids"][0]
    assert len(ids) == 3
    assert ids[0] == content_list["indexed_content_1"].id
    assert ids[1] == content_list["indexed_content_2"].id
    assert ids[2] == content_list["indexed_content_4"].id

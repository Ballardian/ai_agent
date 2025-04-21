import pytest
import tempfile
import shutil
import logging
from spire.doc import Document
from pathlib import Path

# from pathlib import Path
from unittest.mock import Mock, patch

# from datetime import datetime
import click

# from click.testing import CliRunner
from src.backend.database.client.chroma_client import ChromaClient
from utils.document_import_cli import (
    find_word_documents,
    import_document_to_chroma,
    cli,
)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def temp_db_dir():
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    logger.debug(f"Created temporary DB directory: {temp_dir}")
    yield temp_dir
    # Cleanup after test session
    shutil.rmtree(temp_dir)
    logger.debug(f"Removed temporary DB directory: {temp_dir}")


@pytest.fixture
def chroma_client(temp_db_dir):
    client = ChromaClient(collection_name="test_collection", path=temp_db_dir)
    logger.debug(f"Created ChromaClient with path: {temp_db_dir}")
    return client


@pytest.fixture(scope="session", autouse=True)
def temp_document_dir():
    # Create a temporary directory
    temp_doc_dir = tempfile.mkdtemp()
    logger.debug(f"Created temporary document directory: {temp_doc_dir}")
    sample_documents(temp_doc_dir, 3)
    yield temp_doc_dir

    # Cleanup after test session
    shutil.rmtree(temp_doc_dir)
    logger.debug(f"Removed temporary document directory: {temp_doc_dir}")


def sample_documents(path: str, num_docs: int = 3):
    """Create a temporary Word document for testing."""
    logger.debug(f"Creating sample documents in: {path}")
    for i in range(num_docs):
        doc_path = str(path) + f"/test_document_{i}.docx"
        doc = Document()
        section = doc.AddSection()
        paragraph = section.AddParagraph()
        paragraph.AppendText(f"This is test document {i}.")
        # Save the document
        doc.SaveToFile(str(doc_path))
        doc.Close()
    logger.debug(f"Created sample documents at: {path}")


def test_find_word_documents(temp_document_dir):
    logger.debug(f"Testing find_word_documents in: {temp_document_dir}")
    result = find_word_documents(Path(temp_document_dir))
    assert len(result) == 3
    for document in result:
        assert document.suffix == ".docx"
        assert document.name.startswith("test_document_")


def test_import_document_to_chroma(chroma_client, temp_document_dir):
    assert chroma_client.collection.count() == 0
    result = find_word_documents(Path(temp_document_dir))
    # this will be test_document_2.docx
    doc_to_import = result[0]
    logger.debug(f"Found documents: {result}")
    import_document_to_chroma(doc_to_import, chroma_client, "test_subject")
    assert chroma_client.collection.count() == 1
    # get first document
    first_document = chroma_client.get_all_documents()["metadatas"][0]
    assert first_document["name"] == "test_document_2.docx"
    assert first_document["source"] == "word_document"
    assert first_document["subject"] == "test_subject"


# def test_cli_list_docs(mock_chroma_client):
#     # Setup mock Chroma results
#     mock_chroma_client.return_value.fetch_content.return_value = {
#         "ids": [["doc1", "doc2"]],
#         "metadatas": [
#             [
#                 {
#                     "name": "doc1",
#                     "source": "word_document",
#                     "subject": "test",
#                     "date": "2024-01-01",
#                 },
#                 {
#                     "name": "doc2",
#                     "source": "word_document",
#                     "subject": "test",
#                     "date": "2024-01-02",
#                 },
#             ]
#         ],
#     }

#     runner = CliRunner()
#     result = runner.invoke(cli, ["list-docs"])

#     assert result.exit_code == 0
#     assert "Documents in collection:" in result.output
#     assert "doc1" in result.output
#     assert "doc2" in result.output


# def test_cli_query_db(mock_chroma_client):
#     # Setup mock Chroma results
#     mock_chroma_client.return_value.fetch_content.return_value = {
#         "ids": [["doc1"]],
#         "metadatas": [
#             [
#                 {
#                     "name": "doc1",
#                     "source": "word_document",
#                     "subject": "test",
#                     "date": "2024-01-01",
#                 }
#             ]
#         ],
#     }

#     runner = CliRunner()
#     result = runner.invoke(
#         cli, ["query-db", "--query", "test query", "--subject", "test"]
#     )

#     assert result.exit_code == 0
#     assert "Documents in collection:" in result.output
#     assert "doc1" in result.output


# def test_cli_import_docs_nonexistent_path():
#     runner = CliRunner()
#     result = runner.invoke(
#         cli,
#         ["import-docs", "--path", "/nonexistent/path"],
#     )

#     assert result.exit_code != 0
#     assert "Error: Path" in result.output


# def test_cli_import_docs_no_documents(tmp_path):
#     runner = CliRunner()
#     result = runner.invoke(
#         cli,
#         ["import-docs", "--path", str(tmp_path)],
#     )

#     assert result.exit_code == 0
#     assert "No Word documents found" in result.output

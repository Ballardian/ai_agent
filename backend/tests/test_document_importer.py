import pytest
from spire.doc import Document
from backend.database.client.document_importer import DocumentImporter


@pytest.fixture
def sample_doc_path(tmp_path):
    """Create a temporary Word document for testing."""
    doc_path = tmp_path / "test_document.docx"

    # Create a simple Word document using Spire.Doc
    doc = Document()
    section = doc.AddSection()
    paragraph = section.AddParagraph()
    paragraph.AppendText("This is a test document.")
    # Save the document
    doc.SaveToFile(str(doc_path))
    doc.Close()

    return str(doc_path)


def test_extract_text_from_doc(sample_doc_path):
    """Test that text can be extracted from a Word document."""
    importer = DocumentImporter()
    text = importer.extract_text_from_doc(sample_doc_path)
    print("TEXT", text)

    assert text.strip() == "This is a test document."


def test_extract_text_from_nonexistent_file():
    """Test that appropriate error is raised when file doesn't exist."""
    importer = DocumentImporter()
    with pytest.raises(Exception):
        importer.extract_text_from_doc("nonexistent_file.docx")


# def test_extract_text_from_invalid_file(tmp_path):
#     """Test that appropriate error is raised when file is not a valid Word document."""
#     # Create an invalid file
#     invalid_path = tmp_path / "invalid.pdf"
#     with open(invalid_path, "w") as f:
#         f.write("This is not a valid Word document")

#     importer = DocumentImporter()
#     with pytest.raises(Exception):
#         importer.extract_text_from_doc(str(invalid_path))

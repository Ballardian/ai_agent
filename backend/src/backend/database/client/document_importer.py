from spire.doc import Document

# TODO: handle different word document structures
# e.g. tables, images, etc.


# Note: only handles word documents for now
class DocumentImporter:
    def __init__(self):
        pass

    def extract_text_from_doc(self, doc_path: str) -> str:
        """
        Extract text content from a Word document.

        Args:
            doc_path (str): Path to the Word document

        Returns:
            str: Extracted text content from the document
        """
        # Create a Document object
        doc = Document()

        # Load the Word document
        doc.LoadFromFile(doc_path)

        # Extract text from the document
        text = doc.GetText()
        cleaned_text = text.replace(
            "Evaluation Warning: The document was created with Spire.Doc for Python.",
            "",
        )

        # Close the document
        doc.Close()

        return cleaned_text

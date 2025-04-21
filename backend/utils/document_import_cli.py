from pathlib import Path
from datetime import datetime
from typing import List
import click
from backend.database.client.document_importer import DocumentImporter
from backend.database.client.chroma_client import ChromaClient
from backend.database.client.indexed_content import IndexedContent


def find_word_documents(directory: Path) -> List[Path]:
    """Find all .docx files in the given directory and its subdirectories."""
    return list(directory.rglob("*.docx"))


def import_document_to_chroma(
    doc_path: Path, chroma_client: ChromaClient, subject: str
) -> None:
    """Import a single document into Chroma."""
    importer = DocumentImporter()
    text = importer.extract_text_from_doc(str(doc_path))

    # Create indexed content
    content = IndexedContent(
        name=doc_path.name,
        content=text,
        source="word_document",
        date=datetime.now(),
        subject=subject,
    )

    # Add to Chroma
    chroma_client.add_content(content)
    print(f"Imported: {doc_path.name}")


@click.group()
def cli():
    """Word Document Management CLI"""
    pass


@cli.command()
@click.option(
    "--collection", default="teacher_documents", help="Chroma collection name"
)
@click.option(
    "--path",
    default="/Users/georgeballard/Documents/ai_agent_word_docs",
    help="Path to scan for Word documents",
)
@click.option("--subject", default="english", help="Subject of the documents")
# Note: to run this call python -m utils.document_import_cli import-docs
def import_docs(collection: str, path: str, subject: str):
    """Import Word documents from the specified path into Chroma."""
    path = Path(path)

    if not path.exists():
        click.echo(f"Error: Path {path} does not exist")
        return

    click.echo(f"Scanning for Word documents in {path}...")
    documents = find_word_documents(path)

    if not documents:
        click.echo("No Word documents found.")
        return

    click.echo(f"Found {len(documents)} Word documents.")
    chroma_client = ChromaClient(collection_name=collection)

    for doc in documents:
        try:
            import_document_to_chroma(doc, chroma_client, subject)
        except Exception as e:
            click.echo(f"Error importing {doc.name}: {str(e)}")


@cli.command()
@click.option(
    "--collection", default="teacher_documents", help="Chroma collection name"
)
# Note: to run this call python -m utils.document_import_cli list-docs
def list_docs(collection: str):
    """List all documents in the Chroma collection."""
    chroma_client = ChromaClient(collection_name=collection)
    results = chroma_client.get_all_documents()

    if not results["ids"]:
        click.echo("No documents found in the collection.")
        return

    click.echo("\nDocuments in collection:")
    click.echo("----------------------")
    for i, (doc_id, metadata) in enumerate(
        zip(results["ids"][0], results["metadatas"][0]), 1
    ):
        click.echo(f"{i}. {metadata['name']}")
        click.echo(f"   Source: {metadata['source']}")
        click.echo(f"   Subject: {metadata['subject']}")
        click.echo(f"   Date: {metadata['date']}")
        click.echo(f"   ID: {doc_id}")
        click.echo("----------------------")


@cli.command()
@click.option(
    "--collection", default="teacher_documents", help="Chroma collection name"
)
@click.option("--query", default="", help="Query to search for")
@click.option("--subject", default="", help="Subject to filter results")
# Note: to run this call python -m utils.word_doc_cli query-db
def query_db(collection: str, query: List[str], subject: str):
    """List all documents in the Chroma collection."""
    chroma_client = ChromaClient(collection_name=collection)
    results = chroma_client.fetch_content(
        query_texts=query, n_results=3, where={"subject": subject}
    )

    if not results["ids"]:
        click.echo("No documents found in the collection.")
        return

    click.echo("\nDocuments in collection:")
    click.echo("----------------------")
    for i, (doc_id, metadata) in enumerate(
        zip(results["ids"][0], results["metadatas"][0]), 1
    ):
        click.echo(f"{i}. {metadata['name']}")
        click.echo(f"   Source: {metadata['source']}")
        click.echo(f"   Subject: {metadata['subject']}")
        click.echo(f"   Date: {metadata['date']}")
        click.echo(f"   ID: {doc_id}")
        click.echo("----------------------")


if __name__ == "__main__":
    cli()

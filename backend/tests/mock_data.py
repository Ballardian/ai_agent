from src.backend.database.client.indexed_content import IndexedContent

indexed_content_1 = IndexedContent(
    content="This is a document about the book Of Mice and Men",
    name="Of Mice and Men",
    source="book",
    subject="english",
)
indexed_content_2 = IndexedContent(
    content="This is a document about the book To Kill a Mockingbird",
    name="To Kill a Mockingbird",
    source="book",
    subject="english",
)
indexed_content_3 = IndexedContent(
    content="This is a document about the book Madeline",
    name="Madeline",
    source="book",
    subject="french",
)
indexed_content_4 = IndexedContent(
    content="This is a document about how to make a baguette",
    name="How to make a baguette",
    source="recipe",
    subject="english",
)


def get_mock_data():
    return {
        "indexed_content_1": indexed_content_1,
        "indexed_content_2": indexed_content_2,
        "indexed_content_3": indexed_content_3,
        "indexed_content_4": indexed_content_4,
    }

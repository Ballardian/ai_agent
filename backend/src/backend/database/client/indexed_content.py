import uuid
from datetime import datetime
from typing import Dict, Any
from dataclasses import dataclass, field


@dataclass
class IndexedContent:
    """
    Represents content to be indexed in the vector store.
    """

    name: str
    content: str
    source: str
    subject: str
    date: datetime = field(default_factory=datetime.now)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the indexed content to a dictionary for storage.
        """
        return {
            "id": self.id,
            "name": self.name,
            "content": self.content,
            "source": self.source,
            "subject": self.subject,
            "date": self.date.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "IndexedContent":
        """
        Create an IndexedContent instance from a dictionary.
        """
        if isinstance(data.get("date"), str):
            data["date"] = datetime.fromisoformat(data["date"])
        return cls(**data)

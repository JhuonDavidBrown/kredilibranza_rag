from abc import ABC, abstractmethod
from typing import List, Protocol,Any,Dict

from app.core import models


class DocumentRepositoryPort(ABC):
    @abstractmethod
    def save_document(self, document: models.Document) -> None:
        pass

    @abstractmethod
    def get_documents(self, query: str, n_results: int | None = None) -> List[models.Document]:
        pass

    def delete_document(self, document_id: str) -> None:
        pass


class LlmPort(ABC):
    @abstractmethod
    def generate_text(self, prompt: str, retrieval_context: str) -> str:
        pass


class FormRepositoryPort(Protocol):
    async def insert_form_submission(self, data: Dict[str, Any]) -> Any:
        pass

    async def get_form_submission(self, submission_id: str) -> Dict[str, Any]:
        pass
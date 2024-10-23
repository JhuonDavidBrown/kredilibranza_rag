from app.adapters.openai_adapter import OpenAIAdapter
from app.adapters.chromadb_adapter import ChromaDBAdapter
from app import usecases
from app import configurations

from app.adapters.document_extractors import PDFTextExtractorAdapter, DocxTextExtractorAdapter
from app.usecases import DocumentService
from fastapi import UploadFile, HTTPException

from app.adapters.mongodb_adapter import MongoDBAdapter
from app.usecases import FormSubmissionService
from app.configurations import Configs


class RAGServiceSingleton:
    _instance = None

    @classmethod
    def get_instance(cls) -> usecases.RAGService:
        if cls._instance is None:
            configs = configurations.Configs()
            openai_adapter = OpenAIAdapter(api_key=configs.openai_api_key, model=configs.model,
                                           max_tokens=configs.max_tokens, temperature=configs.temperature)
            document_repo = ChromaDBAdapter(number_of_vectorial_results=configs.number_of_vectorial_results)
            cls._instance = usecases.RAGService(document_repo=document_repo, openai_adapter=openai_adapter)
        return cls._instance


def get_document_service(file: UploadFile) -> DocumentService:
    if file.content_type == 'application/pdf':
        text_extractor = PDFTextExtractorAdapter()  # Estrategia para PDF
    elif file.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        text_extractor = DocxTextExtractorAdapter()  # Estrategia para DOCX
    else:
        raise HTTPException(status_code=400, detail="Formato de archivo no soportado")

    return DocumentService(text_extractor)

class FormServiceSingleton:
    _instance = None
    _configs = None

    @classmethod
    def get_instance(cls) -> FormSubmissionService:
        if cls._instance is None:
            # Inicializar configuraciones
            cls._configs = Configs()

            # Inicializar el repositorio
            form_repository = MongoDBAdapter()

            # Crear instancia del servicio con todas sus dependencias
            cls._instance = FormSubmissionService(
                form_repository=form_repository,
                configs=cls._configs
            )
        return cls._instance
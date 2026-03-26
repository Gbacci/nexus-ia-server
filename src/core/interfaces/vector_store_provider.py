from abc import ABC, abstractmethod
from typing import List

class VectorStoreProvider(ABC):
    """
    Interface base para bancos de dados vetoriais (ex: Supabase, Pinecone, Qdrant).
    Permite injetar contexto (Retrieve) para o RAG.
    """
    @abstractmethod
    async def search_similar(self, query_vector: List[float], limit: int = 5, repository_id: str = None) -> List[str]:
        """
        Busca os pedaços de texto (chunks) mais similares com base no vetor da requisição.
        Pode filtrar opcionalmente por um repositório_id específico.
        """
        raise NotImplementedError

    @abstractmethod
    def insert_chunks(self, chunks_data: List[dict]):
        """
        Insere os chunks no banco de dados.
        chunks_data deve conter {'file_path', 'content', 'embedding', 'repository_id'}
        """
        raise NotImplementedError

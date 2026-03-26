from abc import ABC, abstractmethod
from typing import List

class EmbeddingProvider(ABC):
    """
    Interface base para provedores de geração de Embeddings (ex: OpenAI, Cohere).
    Transforma texto livre em representações vetoriais.
    """
    @abstractmethod
    async def embed_query(self, text: str) -> List[float]:
        """
        Recebe a pergunta do usuário e devolve o array/vetor de embeddings.
        """
        raise NotImplementedError

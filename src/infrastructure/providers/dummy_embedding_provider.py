from typing import List
from src.core.interfaces.embedding_provider import EmbeddingProvider

class DummyEmbeddingProvider(EmbeddingProvider):
    """
    Simulador (Mock) de um provedor de Embedding (OpenAI, HuggingFace, etc).
    """
    async def embed_query(self, text: str) -> List[float]:
        # Simulamos que fomos até a API de embeddings e voltamos com um vetor 3D de ponto flutuante
        print(f"[DummyEmbedding] Vetorizando o texto: '{text}'...")
        return [0.12, 0.45, 0.89]

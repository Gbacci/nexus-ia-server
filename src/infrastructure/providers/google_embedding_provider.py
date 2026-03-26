import os
from typing import List
import google.generativeai as genai
from src.core.interfaces.embedding_provider import EmbeddingProvider

class GoogleEmbeddingProvider(EmbeddingProvider):
    """
    Provedor real de Embeddings utilizando os modelos do Google (Gemini).
    """
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY não está configurada para uso nos Embeddings.")
        
        genai.configure(api_key=api_key)
        self.model_name = "models/text-embedding-004"

    async def embed_query(self, text: str) -> List[float]:
        # Chamada à API nativa de embeddings do Google
        # Pode bloquear se for chamada síncrona na lib antiga, mas no geral genai lida bem, ou envelopamos async se necessário.
        response = genai.embed_content(
            model=self.model_name,
            content=text,
            task_type="retrieval_query"
        )
        # Retorna o vetor (lista de floats com 768 dimensões padrão do text-embedding-004)
        return response['embedding']

from typing import List
from src.core.interfaces.vector_store_provider import VectorStoreProvider

class DummyVectorProvider(VectorStoreProvider):
    """
    Simulador (Mock) de um Vector DB (Supabase/PgVector, Pinecone, etc).
    """
    async def search_similar(self, query_vector: List[float], limit: int = 5) -> List[str]:
        print(f"[DummyVectorDB] Buscando documentos matematicamente similares ao vetor {query_vector}...")
        
        # Simulamos o retorno do banco de dados vetorial de chunks de código parecidos
        return [
            "class VectorStoreProvider:\n  # Interface que você está usando agora mesmo!\n  pass",
            "A arquitetura Nexus IA usa FastAPI, Clean Architecture e adaptadores para o LLM."
        ]

from src.core.use_cases.chat_rag_use_case import ChatRagUseCase
from src.infrastructure.factories.llm_factory import LLMFactory
from src.infrastructure.providers.google_embedding_provider import GoogleEmbeddingProvider
from src.infrastructure.providers.postgres_vector_provider import PostgresVectorProvider

class SystemFactory:
    """
    Fábrica agregadora de Injeção de Dependências.
    Ela constrói e retorna Casos de Uso completamente montados 
    com seus devidos provedores (LLM, Embedding, VectorStore).
    """
    @staticmethod
    def get_chat_rag_use_case() -> ChatRagUseCase:
        # 1. Instanciar LLM utilizando a factory já existente
        llm_provider = LLMFactory.get_provider()
        
        # 2. Instanciar Providers de Embeddings e Vetores REAIS (SQLAlchemy + Gemini API)
        embedding_provider = GoogleEmbeddingProvider()
        vector_provider = PostgresVectorProvider()
        
        # 3. Retornar e injetar todos eles no Caso de Uso centralizado
        return ChatRagUseCase(
            llm_provider=llm_provider,
            embedding_provider=embedding_provider,
            vector_store=vector_provider
        )

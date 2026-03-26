from src.core.interfaces.llm_provider import LLMProvider
from src.core.interfaces.embedding_provider import EmbeddingProvider
from src.core.interfaces.vector_store_provider import VectorStoreProvider

class ChatRagUseCase:
    """
    Caso de Uso centralizado para o fluxo RAG (Retrieval-Augmented Generation).
    Gerencia a obtenção da pergunta, extração de contexto vetorial e chamada final ao LLM.
    """
    def __init__(
        self,
        llm_provider: LLMProvider,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStoreProvider
    ):
        self.llm = llm_provider
        self.embedder = embedding_provider
        self.vector_store = vector_store

    async def execute(self, user_message: str, repository_id: str = None) -> str:
        # Se o repositório não for especificado pelo FrontEnd, blindamos a busca 
        # para que NUNCA busque em 'todos', evitando vazamento de contexto Cross-Tenant.
        if not repository_id:
            repository_id = "nexus-ia-mobile"
            
        # Passo 1: Converter a mensagem do usuário em vetor numérico
        query_vector = await self.embedder.embed_query(user_message)
        
        # Passo 2: Buscar Pedaços de Código salvos no banco. Filtra pelo repositório selecionado.
        context_chunks = await self.vector_store.search_similar(query_vector, limit=3, repository_id=repository_id)
        
        # Passo 3: Montar o System Prompt injetando as regras (Prompt Engineering)
        if context_chunks:
            context_text = "\n\n--- CONTEXTO EXTRAÍDO DOS ARQUIVOS ---\n\n".join(context_chunks)
            system_prompt = (
                "Você é um Engenheiro de Software Sênior analisando a arquitetura de projetos do Github.\n"
                "Utilize SOMENTE as informações de contexto abaixo caso sejam relevantes "
                "para responder à pergunta do usuário.\n\n"
                f"{context_text}"
            )
        else:
            system_prompt = (
                "Você é um Engenheiro de Software Sênior respondendo a dúvidas "
                "gerais sobre projetos. Responda de forma sucinta e profissional."
            )
            
        # Passo 4: Chamar a IA com a mensagem do user + context injection no system_prompt
        response = await self.llm.ask(prompt=user_message, system_prompt=system_prompt)
        
        return response

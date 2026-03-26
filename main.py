from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

from src.infrastructure.factories.llm_factory import LLMFactory
from src.core.interfaces.llm_provider import LLMProvider
from src.infrastructure.factories.system_factory import SystemFactory
from src.services.ingestion_service import IngestionService

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = FastAPI(title="Nexus IA Backend (RAG Enabled)")

# Configuração do CORS
# Permite que aplicações externas como o Flutter façam requisições ao servidor
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa o caso de uso pronto, já com todos os provedores embutidos.
try:
    chat_rag_use_case = SystemFactory.get_chat_rag_use_case()
except Exception as e:
    print(f"Aviso na inicialização do sistema: {e}")
    chat_rag_use_case = None

# Modelo de entrada definido com Pydantic para a tipagem dos dados recebidos no corpo
class ChatRequest(BaseModel):
    message: str
    repository_id: str = None

class SyncRequest(BaseModel):
    access_token: str
    repo_ids: List[str]

@app.post("/sync/github")
async def sync_github_repos(request: SyncRequest, background_tasks: BackgroundTasks):
    """
    Endpoint para sincronizar múltiplos repositórios do GitHub.
    Usa BackgroundTasks para iniciar a ingestão RAG sem prender a resposta da API.
    """
    try:
        service = IngestionService()
        background_tasks.add_task(
            service.sync_repos, 
            request.access_token, 
            request.repo_ids
        )
        return {"message": "Sincronização de repositórios iniciada em segundo plano.", "status": "processing"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao iniciar sincronização: {str(e)}")

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if not chat_rag_use_case:
        raise HTTPException(
            status_code=500, 
            detail="Sistema RAG não configurado corretamente no servidor."
        )
        
    try:
        # A rota (Presentation) não sabe qual LLM, Nem de VectorDB, nem de Embedding.
        # Apenas invoca o Caso de Uso passando a mensagem! (Clean Architecture Total)
        reply_text = await chat_rag_use_case.execute(request.message, request.repository_id)
        
        return {"response": reply_text}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno de comunicação com a IA: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Nexus IA Server API (FastAPI) está em execução com Clean Architecture!"}

import asyncio
from dotenv import load_dotenv
from src.infrastructure.factories.system_factory import SystemFactory

load_dotenv()

async def test_rag():
    print("Iniciando teste local RAG...")
    
    # 1. Obter a Use Case agregada (System Factory inicializa Embedder e Vector DB Mocks + LLM Real)
    try:
        use_case = SystemFactory.get_chat_rag_use_case()
    except Exception as e:
        print(f"Erro ao instanciar SystemFactory: {e}")
        return
        
    # 2. Executar uma pergunta teste no RAG Use Case
    pergunta = "Como funciona a interface Provider no seu código atual?"
    print(f"Pergunta: {pergunta}")
    
    try:
        resposta = await use_case.execute(pergunta)
        print("\n=== RESPOSTA DA IA ===")
        print(resposta)
    except Exception as e:
        print(f"Erro ao executar Use Case: {e}")

if __name__ == "__main__":
    asyncio.run(test_rag())

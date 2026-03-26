import asyncio
from dotenv import load_dotenv

load_dotenv()

from src.infrastructure.providers.google_embedding_provider import GoogleEmbeddingProvider
from src.infrastructure.providers.postgres_vector_provider import PostgresVectorProvider
from src.infrastructure.providers.github_provider import GitHubProvider

class IngestionService:
    """
    Serviço de Ingestão RAG.
    Usa a API do Github em memória para buscar arquivos, os fatia e insere no Vector DB.
    """
    def __init__(self):
        self.embedding_provider = GoogleEmbeddingProvider()
        self.vector_store = PostgresVectorProvider()
        self.github_provider = GitHubProvider()

    def _chunk_content(self, file_content: str, lines_per_chunk=150) -> list:
        lines = file_content.split('\n')
        chunks = []
        for i in range(0, len(lines), lines_per_chunk - 20):
            chunk_lines = lines[i:i + lines_per_chunk]
            if not chunk_lines:
                continue
            chunks.append("\n".join(chunk_lines))
        return chunks

    async def sync_repos(self, access_token: str, repo_ids: list[str]):
        print("=== INICIANDO SINCRONIZAÇÃO EM BACKGROUND DO GITHUB ===")
        
        for repo_id in repo_ids:
            print(f"[*] Processando repositório ID: {repo_id} via API in-memory...")
            
            # 1. Obter todo o conteúdo de texto dos arquivos via API
            extracted_files = self.github_provider.get_repository_content(access_token, repo_id)
            print(f"[+] Total de arquivos de código encontrados: {len(extracted_files)}")

            # 2. Chunking
            code_chunks = []
            for file_data in extracted_files:
                chunks = self._chunk_content(file_data['content'])
                for chunk_text in chunks:
                    code_chunks.append({
                        'file_path': file_data['file_path'],
                        'content': chunk_text
                    })
            
            print(f"[+] Total de fatias geradas para {repo_id}: {len(code_chunks)}")

            # 3. Gerar Embeddings
            print("[*] Gerando Embeddings no Cloud...")
            records_to_insert = []
            for chunk in code_chunks:
                vector = await self.embedding_provider.embed_query(chunk['content'])
                records_to_insert.append({
                    'repository_id': str(repo_id),
                    'file_path': chunk['file_path'],
                    'content': chunk['content'],
                    'embedding': vector
                })
            
            # 4. Inserir no PostgreSQL com repo_id anexado
            print(f"[*] Inserindo registros vetorizados no Postgres para {repo_id}...")
            self.vector_store.insert_chunks(records_to_insert)
        
        print("=== SINCRONIZAÇÃO EM BACKGROUND CONCLUÍDA! ===")

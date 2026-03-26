import os
from typing import List
from sqlalchemy.orm import Session
from src.core.interfaces.vector_store_provider import VectorStoreProvider

from src.infrastructure.database.config import engine, SessionLocal
from src.infrastructure.database.models import Base, CodeEmbedding

class PostgresVectorProvider(VectorStoreProvider):
    """
    Provedor real de VectorDB para PostgreSQL com pgvector (Docker/Supabase).
    Agora usa `SessionLocal` global mantendo a escalabilidade sem criar tabelas internamente.
    """
    def __init__(self):
        # engine agora vem do config.py
        pass

    async def search_similar(self, query_vector: List[float], limit: int = 5, repository_id: str = None) -> List[str]:
        """
        Busca usando Cosine Distance (<=> no pgvector).
        Retornará a string formatada com os trechos dos arquivos usando o ORM do SQLAlchemy.
        """
        with SessionLocal() as session:
            query = session.query(CodeEmbedding)
            
            # Filtro opcional pelo Github Repo ID (Pra não misturar contextos de projetos)
            if repository_id:
                query = query.filter(CodeEmbedding.repository_id == repository_id)
                
            # Order by cosine distance (embedding <=> vector)
            results = query.order_by(
                CodeEmbedding.embedding.cosine_distance(query_vector)
            ).limit(limit).all()
            
            chunks = []
            for r in results:
                chunks.append(f"Arquivo: {r.file_path}\nConteúdo:\n{r.content}")
                
            return chunks

    def insert_chunks(self, chunks_data: List[dict]):
        """
        Método extra usado pelo Ingestion Service para salvar as fatias.
        chunks_data = [{'file_path': str, 'content': str, 'embedding': List[float], 'repository_id': str}]
        """
        with SessionLocal() as session:
            for item in chunks_data:
                record = CodeEmbedding(
                    repository_id=item['repository_id'],
                    file_path=item['file_path'],
                    content=item['content'],
                    embedding=item['embedding']
                )
                session.add(record)
            session.commit()

import os
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from pgvector.sqlalchemy import Vector
from src.core.interfaces.vector_store_provider import VectorStoreProvider

Base = declarative_base()

class CodeEmbedding(Base):
    __tablename__ = 'code_embeddings'
    id = Column(Integer, primary_key=True)
    file_path = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    # repository_id para filtro de busca (Multitenant/Repo)
    repository_id = Column(String(100), index=True, nullable=False)
    # text-embedding-004 do Google tem 768 dimensões nativamente
    embedding = Column(Vector(768))

class PostgresVectorProvider(VectorStoreProvider):
    """
    Provedor real de VectorDB para PostgreSQL com pgvector (Docker/Supabase).
    """
    def __init__(self):
        use_docker = os.getenv("USE_DOCKER", "True").lower() == "true"
        
        if use_docker:
            db_url = os.getenv("LOCAL_DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/nexus_ia")
        else:
            db_url = os.getenv("SUPABASE_DATABASE_URL")
            if not db_url:
                raise ValueError("SUPABASE_DATABASE_URL não configurada no .env")
        
        # Ajuste para psycopg2
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
            
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        # Cria as tabelas se não existirem + extensão pgvector se for primeira vez
        self._init_db()

    def _init_db(self):
        with self.engine.connect() as conn:
            conn.execute(Base.metadata.schema_obj._text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()
            
        # [Atenção] Como a estrutura da tabela mudou (adicionamos repository_id Não Nulo),
        # em dev nós dropamos a tabela para recriar o Schema do zero.
        # Em produção, você deverá usar Alembic Migration.
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    async def search_similar(self, query_vector: List[float], limit: int = 5, repository_id: str = None) -> List[str]:
        """
        Busca usando Cosine Distance (<=> no pgvector).
        Retornará a string formatada com os trechos dos arquivos usando o ORM do SQLAlchemy.
        """
        with self.SessionLocal() as session:
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
        with self.SessionLocal() as session:
            for item in chunks_data:
                record = CodeEmbedding(
                    repository_id=item['repository_id'],
                    file_path=item['file_path'],
                    content=item['content'],
                    embedding=item['embedding']
                )
                session.add(record)
            session.commit()

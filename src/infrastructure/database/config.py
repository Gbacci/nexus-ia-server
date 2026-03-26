import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carrega var variáveis antes de usar db_url
load_dotenv()

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

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

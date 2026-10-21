import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine


def get_engine():
    """Cria uma conexão com o MySQL usando as variáveis do arquivo .env."""
    load_dotenv()

    return create_engine(
        URL.create(
            "mysql+mysqlconnector",
            username=os.getenv("GESTAODADOS_DB_USER", "root"),
            password=os.getenv("GESTAODADOS_DB_PASSWORD", ""),
            host=os.getenv("GESTAODADOS_DB_HOST", "127.0.0.1"),
            port=int(os.getenv("GESTAODADOS_DB_PORT", "3306")),
            database=os.getenv("GESTAODADOS_DB_NAME", "gestaodados"),
        ),
        pool_pre_ping=True,
    )

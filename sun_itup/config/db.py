import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class DbConnection:
    _instance = None

    _db_name = os.getenv("DATABASE_NAME")
    _host = os.getenv("DATABASE_HOST")
    _user = os.getenv("DATABASE_USER")
    _password = os.getenv("DATABASE_PASSWORD")
    _port = os.getenv("DATABASE_PORT")

    @classmethod
    def _create_connection(cls):

        cls._instance = psycopg2.connect(
            dbname=cls._db_name,
            host=cls._host,
            user=cls._user,
            password=cls._password,
            port=cls._port
        )

        cls._instance.autocommit = True

    @classmethod
    def get_connection(cls):
        if cls._instance is None:
            cls._create_connection()

        return cls._instance

    @classmethod
    def get_connection_string(cls) -> str:
        return f"postgresql+psycopg2://{cls._user}:{cls._password}@{cls._host}:{cls._port}/{cls._db_name}"

    @classmethod
    def get_async_connection_string(cls) -> str:
        return f"postgresql+asyncpg://{cls._user}:{cls._password}@{cls._host}:{cls._port}/{cls._db_name}"

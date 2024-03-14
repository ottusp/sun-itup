from llama_index.core import get_response_synthesizer
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.response_synthesizers import BaseSynthesizer
from llama_index.llms import OpenAI

from models.embedding_model import embedding_model
from vector_db_retriever import VectorDbRetriever
from vector_store import vector_store

class QueryService:
    @classmethod
    def query(cls) -> None:
        retriever = VectorDbRetriever(
            vector_store=vector_store, embed_model=embedding_model
        )

        query_engine = RetrieverQueryEngine.from_args(
            retriever=retriever,
            response_synthesizer=cls._get_response_synthesizer()
        )
        response = query_engine.query("What is ensemble learning?")

        print(response)

    @classmethod
    def _get_response_synthesizer(cls) -> BaseSynthesizer:
        llm = OpenAI()

        return get_response_synthesizer(llm=llm)

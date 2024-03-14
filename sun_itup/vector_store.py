from llama_index.vector_stores import PGVectorStore

from config.db import DbConnection

vector_store = PGVectorStore.from_params(
    connection_string=DbConnection.get_connection_string(),
    async_connection_string=DbConnection.get_async_connection_string(),
    table_name="items",
    embed_dim=384
)

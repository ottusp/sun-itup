import qdrant_client
from dotenv import load_dotenv
from llama_index import SimpleDirectoryReader, OpenAIEmbedding
from llama_index.embeddings.openai import OpenAIEmbeddingModelType
from llama_index.ingestion import IngestionPipeline
from llama_index.text_splitter import SentenceSplitter
from llama_index.vector_stores import QdrantVectorStore, VectorStoreQuery

load_dotenv()

client = qdrant_client.QdrantClient(location=":memory:")
vector_store = QdrantVectorStore(client=client, collection_name="test_store")

embed_model = OpenAIEmbedding(
    model= OpenAIEmbeddingModelType.TEXT_EMBED_3_SMALL,
    dimensions=512
)

pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=512, chunk_overlap=10),
        embed_model,
    ],
    vector_store=vector_store
)

documents = SimpleDirectoryReader("data").load_data()
nodes = pipeline.run(documents=documents)

query = "What is the conclusion of the article?"

query_embedding = embed_model.get_query_embedding(query)
vs_query = VectorStoreQuery(
    query_embedding=query_embedding, similarity_top_k=2
)

result = vector_store.query(vs_query)

print(result)

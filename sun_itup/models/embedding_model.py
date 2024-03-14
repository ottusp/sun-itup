from llama_index.embeddings import HuggingFaceEmbedding

embedding_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en",
)
from llama_index import SimpleDirectoryReader
from llama_index.core.schema import TextNode, MetadataMode
from llama_index.node_parser import SentenceSplitter

from models.embedding_model import embedding_model
from vector_store import vector_store

class IngestionService:
    @classmethod
    def ingest(cls) -> None:
        documents = SimpleDirectoryReader("sun_itup/data").load_data()

        text_parser = SentenceSplitter(
            chunk_size=512,
            chunk_overlap=10
        )

        text_chunks = []
        doc_indexes = []
        for index, doc in enumerate(documents):
            cur_text_chunks = text_parser.split_text(doc.text)
            text_chunks.extend(cur_text_chunks)
            doc_indexes.extend([index] * len(cur_text_chunks))

        nodes = []
        for index, text_chunk in enumerate(text_chunks):
            node = TextNode(
                text=text_chunk,
            )
            src_doc = documents[doc_indexes[index]]
            node.metadata = src_doc.metadata
            nodes.append(node)

        for node in nodes:
            node_embedding = embedding_model.get_text_embedding(
                node.get_content(metadata_mode=MetadataMode.ALL)
            )

            node.embedding = node_embedding

        vector_store.add(nodes)

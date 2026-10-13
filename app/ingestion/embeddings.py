from functools import lru_cache
from sentence_transformers import SentenceTransformer
from app.ingestion.models import SourceDocument

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

@lru_cache(maxsize=1)
def get_embeddings_model():

    print(f"Loading embedding model '{MODEL_NAME}'...")
    return SentenceTransformer
    

def embed_documents(chunks: list[SourceDocument]):

    if chunks is None:
        return []


    for chunk in chunks:

        embedding = get_embeddings_model(chunk.content)
        embedding.tolist()

    return

a = get_embeddings_model()
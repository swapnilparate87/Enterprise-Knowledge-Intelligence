from functools import lru_cache
from sentence_transformers import SentenceTransformer
from app.ingestion.models import SourceDocument

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

@lru_cache(maxsize=1)
def get_embeddings_model():

    print(f"Loading embedding model '{MODEL_NAME}'...")
    return SentenceTransformer(MODEL_NAME)
    

def embed_documents(chunks: list[SourceDocument]):

    if not chunks:
        return []
    
    model = get_embeddings_model()

    texts = [chunk.content for chunk in chunks]

    embeddings = model.encode(texts)

    return embeddings.tolist()


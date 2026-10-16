from fastapi import FastAPI
from app.api.schemas import AskRequest, AskResponse, SourceItem
from app.ingestion.retrieval import retrieve_chunks
from app.generation.llm import generate_answer

app = FastAPI(title="Enterprise Knowledge Intelligence")

@app.get("/health")
def health():
    return {"status":"Ok", "message": "API is healthy and running!"}

@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    query = request.query

    # Call your existing retrieval function
    chunk = retrieve_chunks(query)

    # Call your existing generation function
    response = generate_answer(query,chunk)

    # Return the response in the expected schema
    return response
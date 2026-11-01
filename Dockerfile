# One image for every role: API, chat UI, ingestion, or both API + UI (default, for single-container hosting).
# Same Python as the tested .venv, so the exact versions in constraints.txt all have wheels.
FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DEFAULT_TIMEOUT=120 \
    PIP_RETRIES=10 \
    DEEPEVAL_TELEMETRY_OPT_OUT=YES

RUN useradd --create-home appuser
WORKDIR /app

# CPU-only PyTorch: the default Linux wheel bundles ~2.5 GB of CUDA libraries this app never uses.
RUN pip install torch==2.15.0 --index-url https://download.pytorch.org/whl/cpu
# Pinned versions: no dependency backtracking, and the container runs exactly what was tested.
COPY requirements.txt constraints.txt ./
RUN pip install -r requirements.txt -c constraints.txt

# Bake the embedding model into the image so containers start without downloading it.
USER appuser
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"

COPY --chown=appuser app ./app
COPY --chown=appuser data ./data
COPY --chown=appuser --chmod=755 start.sh ./

EXPOSE 8000 8501
CMD ["./start.sh"]

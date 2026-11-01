#!/bin/sh
# Single-container mode (e.g. Hugging Face Spaces, Render): API in the background, chat UI in front.
# The UI listens on $PORT if the host sets one, otherwise 8501.
set -e
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
exec streamlit run app/frontend.py --server.address 0.0.0.0 --server.port "${PORT:-8501}" --server.headless true

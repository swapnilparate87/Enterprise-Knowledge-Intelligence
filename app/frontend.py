"""Streamlit chat UI.  Run (with the API running): streamlit run app/frontend.py"""
import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
DEPARTMENTS = ["customer_success", "engineering", "hr", "it_security", "operations"]

st.set_page_config(page_title="Enterprise Knowledge Intelligence", page_icon="📚", layout="wide")
st.title("Enterprise Knowledge Intelligence")
st.caption("Ask questions about company documents. Answers cite their sources.")

with st.sidebar:
    departments = st.multiselect("Search only these departments", DEPARTMENTS)
    if st.button("Clear chat"):
        st.session_state.messages = []

if "messages" not in st.session_state:
    st.session_state.messages = []


def show_sources(sources: list[dict]) -> None:
    if not sources:
        return
    with st.expander(f"Sources ({len(sources)})"):
        for s in sources:
            page = f", page {s['page_number']}" if s.get("page_number") else ""
            rerank = f" · rerank {s['rerank_score']:.2f}" if s.get("rerank_score") is not None else ""
            st.markdown(f"**[{s['source_id']}] {s['doc_id']} - {s['title']}**{page} · similarity {s['similarity']:.2f}{rerank}")
            st.caption(s["content"][:500])


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        show_sources(message.get("sources", []))

if query := st.chat_input("e.g. When do I need a doctor's note for sick leave?"):
    history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Searching documents..."):
                response = requests.post(
                    f"{API_URL}/ask",
                    json={"query": query, "history": history, "departments": departments or None},
                    timeout=200,
                )
            if response.status_code != 200:
                st.error(f"API error {response.status_code}: {response.json().get('detail', response.text)}")
            else:
                result = response.json()
                st.markdown(result["answer"])
                show_sources(result["sources"])
                st.session_state.messages.append(
                    {"role": "assistant", "content": result["answer"], "sources": result["sources"]}
                )
        except requests.RequestException as exc:
            st.error(f"Could not reach the API at {API_URL}: {exc}")

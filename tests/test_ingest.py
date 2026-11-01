"""Unit tests for loading and chunking. No database, model or LLM needed."""
from pathlib import Path

import pytest

from app import config
from app.ingest import Page, chunk_pages, clean_text, discover_files, document_metadata, load_file


def test_document_metadata_parses_id_title_and_department():
    meta = document_metadata(Path("data/hr/HR-001_leave-and-attendance-policy.pdf"))
    assert meta == {"doc_id": "HR-001", "title": "Leave And Attendance Policy", "department": "hr"}


def test_document_metadata_without_id_prefix_uses_stem():
    meta = document_metadata(Path("notes/meeting_notes.txt"))
    assert meta["doc_id"] == "meeting_notes"
    assert meta["department"] == "notes"


def test_clean_text_fixes_pdf_bullets_null_bytes_and_blank_lines():
    raw = "Intro\x00\n�\nFirst item\n\n\n\n\nNext   section"
    assert clean_text(raw) == "Intro\n- First item\n\nNext section"


def test_discover_files_is_recursive_and_filters_extensions(tmp_path):
    (tmp_path / "hr").mkdir()
    for name in ["hr/a.pdf", "hr/b.md", "c.txt", "d.docx", "e.csv", "f.png"]:
        (tmp_path / name).write_bytes(b"x")
    found = {p.name for p in discover_files(tmp_path)}
    assert found == {"a.pdf", "b.md", "c.txt", "d.docx"}


def test_discover_files_rejects_missing_folder(tmp_path):
    with pytest.raises(NotADirectoryError):
        discover_files(tmp_path / "missing")


def test_load_text_file(tmp_path):
    folder = tmp_path / "engineering"
    folder.mkdir()
    path = folder / "ENG-013_dev-setup.md"
    path.write_text("# Dev setup\n\nInstall Python 3.12.", encoding="utf-8")

    [page] = load_file(path)
    assert page.doc_id == "ENG-013"
    assert page.department == "engineering"
    assert page.file_type == "md"
    assert page.page_number is None
    assert "Install Python" in page.text


def test_load_file_rejects_unsupported_type(tmp_path):
    path = tmp_path / "x.csv"
    path.write_text("a,b")
    with pytest.raises(ValueError):
        load_file(path)


def test_chunk_ids_are_unique_and_indexes_continue_across_pages():
    pages = [
        Page("HR-001", "Leave", "hr", "hr/HR-001.pdf", "pdf", page_number, "word " * 400)
        for page_number in (1, 2)
    ]
    rows = chunk_pages(pages, chunk_size=500, chunk_overlap=50)

    assert len(rows) > 2
    assert len({r["chunk_id"] for r in rows}) == len(rows)
    assert [r["chunk_index"] for r in rows] == list(range(len(rows)))
    assert {r["page_number"] for r in rows} == {1, 2}
    assert all(len(r["content"]) <= 500 for r in rows)


@pytest.mark.skipif(not config.DATA_DIR.is_dir(), reason="sample data not present")
def test_every_sample_document_loads_with_text():
    files = discover_files(config.DATA_DIR)
    assert files
    for path in files:
        pages = load_file(path)
        assert pages, f"no text extracted from {path.name}"
        assert pages[0].doc_id.split("-")[0] in {"CS", "ENG", "HR", "SEC", "OPS"}

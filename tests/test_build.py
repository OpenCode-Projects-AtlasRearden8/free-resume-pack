"""Tests for the Free Resume Pack build.

Each check treats the build the way a user would:
  - does every template build at all,
  - is the PDF real and openable,
  - is the text actually selectable (that's what keeps it ATS-friendly),
  - and do mistakes produce plain-English messages, not crashes.
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]

_spec = importlib.util.spec_from_file_location("resume_build", ROOT / "build.py")
resume_build = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(resume_build)

ALL_DOCS = [(variant, doc) for variant in resume_build.VARIANTS for doc in resume_build.DOCS]
SAMPLE_NAME = "Avery Sample"  # the fictitious person shipped in the sample data


@pytest.fixture(scope="session")
def sample_values() -> dict:
    return resume_build.load_values(resume_build.DEFAULT_DATA)


def test_every_template_file_exists():
    for variant, doc in ALL_DOCS:
        path = ROOT / "templates" / variant / f"{doc}.html"
        assert path.exists(), f"missing template: {path}"


def test_every_style_has_css():
    for variant in resume_build.VARIANTS:
        path = ROOT / "templates" / variant / f"{variant}.css"
        assert path.exists(), f"missing stylesheet: {path}"


@pytest.mark.parametrize("variant,doc", ALL_DOCS)
def test_built_pdf_is_real_with_selectable_text(sample_values, tmp_path, variant, doc):
    pdf_path, _ = resume_build.build_document(variant, doc, sample_values, tmp_path)

    assert pdf_path.exists()
    assert pdf_path.read_bytes()[:5] == b"%PDF-", "not a PDF header"

    reader = PdfReader(str(pdf_path))
    assert len(reader.pages) >= 1, "PDF has no pages"

    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert SAMPLE_NAME.lower() in text.lower(), (
        f"{pdf_path.name} lost its text layer (an ATS would see an empty document)"
    )


def test_build_all_creates_exactly_nine_unique_pdfs(sample_values, tmp_path):
    paths = resume_build.build_all(
        list(resume_build.VARIANTS), list(resume_build.DOCS), out_dir=tmp_path
    )
    names = sorted(p.name for p in paths)
    expected = sorted(f"{doc}-{variant}.pdf" for variant, doc in ALL_DOCS)
    assert names == expected
    assert len(set(paths)) == 9


def test_missing_detail_gives_plain_english_error(sample_values, capsys):
    incomplete = dict(sample_values)
    incomplete.pop("email")
    with pytest.raises(resume_build.BuildError) as caught:
        resume_build.build_document("classic", "cover-letter", incomplete, Path("/tmp/opencode/unused"))
    message = str(caught.value)
    assert "email" in message
    assert "Add them to your details file" in message


def test_broken_json_gives_friendly_error(tmp_path):
    bad = tmp_path / "broken-details.json"
    bad.write_text('{"full_name": "Avery Sample", "email": }', encoding="utf-8")
    with pytest.raises(resume_build.BuildError) as caught:
        resume_build.load_values(bad)
    assert "line 1" in str(caught.value)
    assert "valid JSON" in str(caught.value)


def test_comment_keys_starting_with_underscore_are_ignored(tmp_path):
    details_file = tmp_path / "details.json"
    details_file.write_text(
        '{"_note": "not a token", "full_name": "Avery Sample"}', encoding="utf-8"
    )
    loaded = resume_build.load_values(details_file)
    assert "_note" not in loaded
    mapping = resume_build.escaped_mapping(loaded)
    assert mapping["today"]  # the date token fills itself


def test_list_values_become_list_items():
    items = {"job1_bullets": ["Kept a 40-person schedule.", "Wrote clean monthly reports."]}
    rendered = resume_build.escaped_mapping(items)["job1_bullets"]
    assert rendered.count("<li>") == 2 and "<li>Kept a 40-person schedule.</li>" in rendered


def test_sample_documents_build_in_a_row(tmp_path, sample_values):
    """One of each document type builds from the same sample data."""
    for doc in resume_build.DOCS:
        pdf_path, _ = resume_build.build_document("classic", doc, sample_values, tmp_path)
        assert pdf_path.exists() and pdf_path.stat().st_size > 0


def test_sample_data_has_no_real_looking_secrets(sample_values):
    """Guardrail: the sample stays obviously fictitious (no real domains or keys)."""
    blob = json.dumps(sample_values)
    for forbidden in ["@gmail", "password", "api_key", "secret"]:
        assert forbidden not in blob, f"sample data should never contain {forbidden!r}"


def test_command_line_build_end_to_end(tmp_path):
    result = subprocess.run(
        [sys.executable, str(ROOT / "build.py"), "--out", str(tmp_path)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert result.returncode == 0, result.stderr
    pdfs = sorted(p.name for p in tmp_path.glob("*.pdf"))
    assert len(pdfs) == 9

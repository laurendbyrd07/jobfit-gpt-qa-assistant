"""Tests for parser utilities."""

from pathlib import Path

from jobfit.models import ParsedDocument
from jobfit.parser import (
    extract_qa_keywords,
    load_job_description,
    load_resume,
    load_text_file,
    normalize_text,
    parse_text,
)


def test_normalize_text_lowercases_strips_and_collapses_spacing() -> None:
    text = "  Manual   Testing\n& JIRA!!!  Regression\tTesting  "

    assert normalize_text(text) == "manual testing and jira regression testing"


def test_extract_qa_keywords_returns_sorted_unique_matches() -> None:
    text = "Jira, JIRA, manual testing, Selenium, and API testing are required."

    assert extract_qa_keywords(text) == (
        "api testing",
        "jira",
        "manual testing",
        "selenium",
    )


def test_extract_qa_keywords_uses_word_boundaries() -> None:
    text = "The candidate wrote about agiles but not the exact delivery framework term."

    assert "agile" not in extract_qa_keywords(text)


def test_load_text_file_reads_utf8_file(tmp_path: Path) -> None:
    file_path = tmp_path / "resume.txt"
    file_path.write_text("Quality Assurance with pytest", encoding="utf-8")

    content, error = load_text_file(file_path)

    assert content == "Quality Assurance with pytest"
    assert error is None


def test_load_text_file_handles_missing_file_gracefully(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing.txt"

    content, error = load_text_file(missing_path)

    assert content == ""
    assert error == f"File not found: {missing_path}"


def test_load_text_file_handles_directory_path_gracefully(tmp_path: Path) -> None:
    content, error = load_text_file(tmp_path)

    assert content == ""
    assert error == f"Expected a text file but found a directory: {tmp_path}"


def test_parse_text_returns_typed_document() -> None:
    document = parse_text(
        "Created test cases for regression testing in Jira.",
        source_path="inline-resume.txt",
        document_type="resume",
    )

    assert isinstance(document, ParsedDocument)
    assert document.source_path == Path("inline-resume.txt")
    assert document.document_type == "resume"
    assert document.raw_text == "Created test cases for regression testing in Jira."
    assert document.normalized_text == "created test cases for regression testing in jira"
    assert document.keywords == ("jira", "regression testing", "test cases")
    assert document.missing is False
    assert document.error is None


def test_load_resume_parses_resume_file(tmp_path: Path) -> None:
    resume_path = tmp_path / "resume.txt"
    resume_path.write_text("Manual testing and bug reporting with Jira.", encoding="utf-8")

    document = load_resume(resume_path)

    assert document.document_type == "resume"
    assert document.source_path == resume_path
    assert document.raw_text == "Manual testing and bug reporting with Jira."
    assert document.keywords == ("bug reporting", "jira", "manual testing")
    assert document.missing is False
    assert document.error is None


def test_load_job_description_parses_job_file(tmp_path: Path) -> None:
    job_path = tmp_path / "job.txt"
    job_path.write_text("Looking for Selenium, API testing, and CI/CD.", encoding="utf-8")

    document = load_job_description(job_path)

    assert document.document_type == "job_description"
    assert document.source_path == job_path
    assert document.keywords == ("api testing", "ci/cd", "selenium")
    assert document.missing is False
    assert document.error is None


def test_load_resume_returns_missing_document_for_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing-resume.txt"

    document = load_resume(missing_path)

    assert document.document_type == "resume"
    assert document.source_path == missing_path
    assert document.raw_text == ""
    assert document.normalized_text == ""
    assert document.keywords == ()
    assert document.missing is True
    assert document.error == f"File not found: {missing_path}"

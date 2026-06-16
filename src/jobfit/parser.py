"""Parsing utilities for resumes and QA job descriptions."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

from jobfit.models import ParsedDocument

QA_KEYWORDS: tuple[str, ...] = (
    "acceptance criteria",
    "agile",
    "api testing",
    "automation",
    "bug reporting",
    "ci/cd",
    "defect tracking",
    "exploratory testing",
    "functional testing",
    "jira",
    "manual testing",
    "playwright",
    "pytest",
    "quality assurance",
    "regression testing",
    "selenium",
    "smoke testing",
    "test cases",
    "test plans",
    "test strategy",
)

_WHITESPACE_PATTERN = re.compile(r"\s+")
_NON_WORD_BOUNDARY_CHARS = re.compile(r"[^a-z0-9+#/-]+")


def normalize_text(text: str) -> str:
    """Return lowercase text with consistent spacing and punctuation boundaries."""
    normalized = text.lower().replace("&", " and ")
    normalized = _NON_WORD_BOUNDARY_CHARS.sub(" ", normalized)
    return _WHITESPACE_PATTERN.sub(" ", normalized).strip()


def extract_qa_keywords(
    text: str,
    *,
    keywords: Iterable[str] = QA_KEYWORDS,
) -> tuple[str, ...]:
    """Extract known QA keywords from text in deterministic alphabetical order."""
    normalized_text = normalize_text(text)
    matches: set[str] = set()

    for keyword in keywords:
        normalized_keyword = normalize_text(keyword)
        if not normalized_keyword:
            continue

        pattern = rf"(?<!\w){re.escape(normalized_keyword)}(?!\w)"
        if re.search(pattern, normalized_text):
            matches.add(keyword)

    return tuple(sorted(matches))


def load_text_file(path: str | Path) -> tuple[str, str | None]:
    """Load a UTF-8 text file, returning content and an optional error message."""
    file_path = Path(path)

    try:
        return file_path.read_text(encoding="utf-8"), None
    except FileNotFoundError:
        return "", f"File not found: {file_path}"
    except IsADirectoryError:
        return "", f"Expected a text file but found a directory: {file_path}"
    except UnicodeDecodeError:
        return "", f"Unable to decode file as UTF-8 text: {file_path}"
    except OSError as exc:
        return "", f"Unable to read file {file_path}: {exc}"


def parse_text(text: str, *, source_path: str | Path, document_type: str) -> ParsedDocument:
    """Parse raw text into a typed document model."""
    normalized_text = normalize_text(text)
    return ParsedDocument(
        source_path=Path(source_path),
        document_type=document_type,
        raw_text=text,
        normalized_text=normalized_text,
        keywords=extract_qa_keywords(normalized_text),
    )


def parse_file(path: str | Path, *, document_type: str) -> ParsedDocument:
    """Load and parse a text file into a typed document model."""
    raw_text, error = load_text_file(path)
    file_path = Path(path)

    if error is not None:
        return ParsedDocument(
            source_path=file_path,
            document_type=document_type,
            raw_text="",
            normalized_text="",
            keywords=(),
            missing=True,
            error=error,
        )

    return parse_text(raw_text, source_path=file_path, document_type=document_type)


def load_resume(path: str | Path) -> ParsedDocument:
    """Load and parse a resume text file."""
    return parse_file(path, document_type="resume")


def load_job_description(path: str | Path) -> ParsedDocument:
    """Load and parse a job description text file."""
    return parse_file(path, document_type="job_description")

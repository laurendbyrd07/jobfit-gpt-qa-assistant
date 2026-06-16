"""Data models for JobFitGPT QA Assistant."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class ParsedDocument:
    """Structured representation of a parsed text document."""

    source_path: Path
    document_type: str
    raw_text: str
    normalized_text: str
    keywords: tuple[str, ...] = field(default_factory=tuple)
    missing: bool = False
    error: str | None = None

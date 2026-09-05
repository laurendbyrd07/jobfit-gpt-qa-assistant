# JobFitGPT QA Assistant

JobFitGPT QA Assistant is a Python portfolio project designed to compare a candidate resume against a Quality Assurance (QA) job description. The planned application will score the match, identify skill gaps, and generate practical recommendations that help candidates tailor applications for QA roles.

## Project Purpose

The project demonstrates how a structured Python application can support a common job-search workflow for QA professionals:

- Parse resume content and QA job descriptions.
- Compare candidate experience against role requirements.
- Produce an interpretable fit score.
- Highlight missing or underrepresented skills.
- Recommend resume, cover letter, and interview preparation improvements.

This repository currently contains the initial project scaffold only. Business logic will be implemented in later development milestones.

## Planned Features

- Resume and job-description text loading.
- Basic parsing utilities for extracting skills, tools, and experience signals.
- QA-focused scoring model for role alignment.
- Gap analysis for testing skills, automation tools, defect tracking, CI/CD, and domain experience.
- Recommendation generation for resume edits and application strategy.
- Command-line interface for local usage.
- Unit tests for parser, scoring, and analyzer modules.
- Future support for AI-assisted analysis through prompt templates.

## Tech Stack

- **Language:** Python
- **Project layout:** `src/` package structure
- **Testing:** pytest
- **Interface:** Command-line interface planned
- **AI readiness:** Prompt templates and model abstractions planned for future LLM integration
- **Version control:** Git and GitHub pull-request workflow

## Project Structure

```text
.
├── README.md
├── examples/
│   ├── sample_qa_job_description.txt
│   └── sample_resume.txt
├── src/
│   └── jobfit/
│       ├── __init__.py
│       ├── analyzer.py
│       ├── cli.py
│       ├── models.py
│       ├── parser.py
│       ├── prompts.py
│       └── scoring.py
└── tests/
    ├── test_analyzer.py
    ├── test_parser.py
    └── test_scoring.py
```

## Development Roadmap

### Phase 1: Project Foundation

- Create repository structure.
- Add placeholder modules for parsing, scoring, analysis, prompts, models, and CLI entry points.
- Add sample resume and QA job-description files.
- Add placeholder test files.

### Phase 2: Core Parsing

- Implement resume and job-description loading.
- Normalize text input.
- Extract QA skills, tools, certifications, and experience keywords.

### Phase 3: Fit Scoring

- Define scoring categories and weights.
- Implement deterministic scoring logic.
- Add unit tests for scoring edge cases.

### Phase 4: Gap Analysis and Recommendations

- Identify required skills missing from the resume.
- Prioritize high-impact improvements.
- Generate actionable application recommendations.

### Phase 5: CLI and AI Integration

- Add a command-line workflow for comparing files.
- Introduce prompt templates for optional LLM-powered summaries.
- Add model abstractions for future provider integrations.

## Current Status

Initial project structure has been created. Business logic is intentionally not implemented yet.

## QA Perspective

This project is also a portfolio demonstration of QA thinking for AI-enabled systems: how evaluation differs for deterministic vs. probabilistic components, what the quality risks are, and what is tested vs. planned. See [QA_STRATEGY.md](./QA_STRATEGY.md).

**Status note:** this repository currently contains the project scaffold only, as described in QA_STRATEGY.md §0.

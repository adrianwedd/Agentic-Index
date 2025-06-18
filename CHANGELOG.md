# Changelog

All notable changes to this project will be documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
- README table header renamed from **Score** to **Overall**.

### Docs
- Restructured documentation layout (GH-DOC-11a).
- Expanded reference material (GH-DOC-11b).
- Added system architecture diagram and links (GH-DOC-11c).
- Scoring modules moved from `score/` to `lib/quality_metrics.py` with CLI entry point `agentic_index_cli/agentic_index.py` (CR-AI-05).

## [0.1.0] - 2024-05-30
### Added
- Introduced 📊 Metrics Legend.
- Added new scoring columns (maint, stars_7d, etc.).
- README snapshot now uses diff tolerance ±0.02.
[2025-06-18] chore(self-improve): cycle #1 – fixed load_json call, added caching test, documented architecture

# Changelog

All notable changes to lazyenv will be documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] — 2026-06-27

### Added
- Beautiful Textual TUI with syntax-aware key-value viewer
- Auto-discovery of all `.env*` files in a project (respects `.git`, `node_modules`, etc.)
- Secrets masking by default for keys matching common patterns (`API_KEY`, `SECRET`, `PASSWORD`, etc.)
- Side-by-side diff view comparing any two `.env` files
- Validation against `.env.example` with colour-coded status (missing / extra / changed)
- Live search/filter with `/`
- Copy selected value to clipboard with `c`
- Open file in `$EDITOR` with `e`
- Reload all files with `r`
- Status bar showing file count, current file, mask state, and diff mode
- Help overlay with full keyboard reference (`?`)
- CLI mode: `--list`, `--diff FILE1 FILE2`, `--validate ENV EXAMPLE`
- CI-friendly exit codes (exit 1 when validation fails)
- Handles `.env`, `.env.local`, `.env.example`, `.env.production`, `.env.staging`, etc.
- Supports quoted values (single/double), `export` prefix, inline comments, multiline backslash continuation
- Cross-platform: Windows, macOS, Linux

[Unreleased]: https://github.com/lazyenv/lazyenv/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/lazyenv/lazyenv/releases/tag/v0.1.0

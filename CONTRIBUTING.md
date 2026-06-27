# Contributing to lazyenv

Thank you for your interest in contributing! lazyenv is a community project and we welcome all contributions — from bug fixes to new features to documentation improvements.

## Quick start

```bash
# 1. Fork the repo and clone your fork
git clone https://github.com/YOUR_USERNAME/lazyenv.git
cd lazyenv

# 2. Create a virtual environment and install dev dependencies
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

# 3. Run the tests
pytest

# 4. Run lazyenv
lazyenv
```

## Development workflow

1. **Create a branch** from `main`:
   ```bash
   git checkout -b feat/my-feature
   ```

2. **Make your changes** — keep them focused on one thing.

3. **Write or update tests** in `tests/`.

4. **Check code quality**:
   ```bash
   ruff check src/ tests/    # linting
   mypy src/lazyenv           # type checking
   pytest                    # tests
   ```

5. **Open a Pull Request** against `main`.

## Project structure

```
src/lazyenv/
├── __main__.py      CLI entry point (click)
├── app.py           Textual TUI application
├── parser.py        .env file parser
├── diff.py          Diff engine
├── models.py        Data models
├── widgets/         Reusable TUI widgets
│   ├── file_list.py     Sidebar file browser
│   ├── env_detail.py    Key-value viewer
│   ├── diff_view.py     Side-by-side diff
│   └── status_bar.py    Status line
├── screens/
│   └── help.py          Help overlay
└── styles/
    └── main.tcss        Textual CSS styles
```

## Good first issues

Look for issues labelled [`good first issue`](https://github.com/lazyenv/lazyenv/issues?q=label%3A%22good+first+issue%22) or [`help wanted`](https://github.com/lazyenv/lazyenv/issues?q=label%3A%22help+wanted%22).

Some ideas to get you started:

- **New secret key patterns** — add more patterns to `_SECRET_PATTERNS` in `parser.py`
- **Shell completions** — add bash/zsh/fish completion via click
- **More tests** — increase coverage, especially for the TUI
- **New .env format** — support Docker secrets format, Vault KV, etc.
- **Documentation** — improve examples, add a getting started video

## Coding style

- **Python 3.10+** — use `match/case`, `X | Y` unions, `list[str]` instead of `List[str]`
- **Type hints everywhere** — we run mypy in strict mode
- **Ruff** for linting — run `ruff check --fix` to auto-fix
- **No comments explaining what code does** — only add comments for non-obvious *why*

## Questions?

Open a [Discussion](https://github.com/lazyenv/lazyenv/discussions) or join our community. All questions welcome!

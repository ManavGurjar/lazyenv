# lazyenv

> A beautiful, lazygit-inspired TUI for managing `.env` files.

[![PyPI version](https://img.shields.io/pypi/v/lazyenv.svg?color=violet)](https://pypi.org/project/lazyenv/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org)
[![CI](https://github.com/ManavGurjar/lazyenv/actions/workflows/ci.yml/badge.svg)](https://github.com/ManavGurjar/lazyenv/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/lazyenv.svg)](https://pypi.org/project/lazyenv/)

```
┌──────────────────────────────────────────────────────────────────────┐
│ lazyenv                                              12:34:56        │
├─────────────────────┬────────────────────────────────────────────────┤
│ 📁 ENV FILES        │  KEY                 = VALUE                   │
│ ✓ .env              │                                                │
│ ⚠ .env.local        │  # Database                                    │
│ · .env.example      │  DATABASE_URL        = postgres://localhost/db  │
│ ✓ services/api/.env │  DB_PASSWORD         = ••••••••••••            │
│                     │                                                │
│                     │  # API Keys                                    │
│                     │  STRIPE_SECRET_KEY   = ••••••••••••            │
│                     │  OPENAI_API_KEY      = ••••••••••••            │
│                     │                                                │
│                     │  # App config                                  │
│                     │  APP_ENV             = development             │
│                     │  APP_PORT            = 3000                    │
│                     │  DEBUG               = false                   │
├─────────────────────┴────────────────────────────────────────────────┤
│ lazyenv  .env  │  4 files  │  MASK ON  │                            │
│  q Quit  d Diff  m Mask  c Copy  e Edit  / Filter  ? Help           │
└──────────────────────────────────────────────────────────────────────┘
```

**Stop guessing which keys are missing.** lazyenv gives you a real-time, searchable, side-by-side view of all your `.env` files — with instant diff against `.env.example` and secrets masked by default.

## Why lazyenv?

Every developer has been there:

- 😤 Cloned a repo, spent 20 minutes figuring out which env vars to set
- 😤 Deployed to staging and got a cryptic error because one key was missing  
- 😤 Shared your `.env` with a teammate and accidentally included a secret
- 😤 Lost track of which keys are in `.env` vs `.env.local` vs `.env.production`

lazyenv fixes all of this.

## Features

- **Beautiful TUI** — keyboard-driven interface inspired by lazygit
- **Auto-discovery** — finds all `.env*` files recursively in your project
- **Secrets masking** — sensitive keys (`API_KEY`, `SECRET`, `PASSWORD`, etc.) are masked by default
- **Side-by-side diff** — instantly compare any two `.env` files
- **Validation** — highlights missing/extra/changed keys vs `.env.example`
- **Live search** — filter keys in real-time with `/`
- **Copy to clipboard** — `c` copies the selected value
- **Open in editor** — `e` opens the file in your `$EDITOR`
- **CLI mode** — non-interactive `--diff` and `--validate` commands for CI pipelines
- **Cross-platform** — Windows, macOS, Linux

## Installation

```bash
# pip
pip install lazyenv

# uv (recommended)
uv tool install lazyenv

# pipx
pipx install lazyenv
```

### One-liner (no install)

```bash
uvx lazyenv
```

### Pre-built binaries

Download from the [latest release](https://github.com/ManavGurjar/lazyenv/releases/latest) — no Python required.

## Usage

```bash
# Open TUI in current directory
lazyenv

# Open TUI in a specific project
lazyenv /path/to/my/project

# Short alias
le

# List all .env files (no TUI)
lazyenv --list

# Diff two files (CI-friendly, exits 1 if different)
lazyenv --diff .env .env.example

# Validate .env against .env.example
lazyenv --validate .env .env.example
```

## Keyboard Reference

| Key | Action |
|-----|--------|
| `↑/↓` | Navigate |
| `Tab` | Switch panel (file list ↔ content) |
| `d` | Toggle diff view |
| `m` | Toggle secret masking |
| `/` or `f` | Filter keys |
| `c` | Copy selected value to clipboard |
| `e` | Open in `$EDITOR` |
| `r` | Reload all files |
| `?` | Help |
| `q` | Quit |

## Diff View

Press `d` to enter diff mode. lazyenv automatically selects `.env.example` (or `.env.sample`) as the reference.

```
┌──────────────────┬─────────────────────────┬─────────────────────────┐
│ KEY              │ REFERENCE (.env.example)│ CURRENT (.env)          │
├──────────────────┼─────────────────────────┼─────────────────────────┤
│   DATABASE_URL   │ postgres://localhost/db  │ postgres://localhost/db  │
│ ✗ STRIPE_KEY     │ (empty)                 │ (absent)                │
│ ~ APP_PORT       │ 3000                    │ 8080                    │
│ + INTERNAL_FLAG  │ (absent)                │ true                    │
└──────────────────┴─────────────────────────┴─────────────────────────┘
  ✗ 1 missing  ~ 1 changed  + 1 extra  ✓ 8 matching
```

## CLI Mode (CI Integration)

```bash
# In your CI pipeline — exits with code 1 if .env is missing keys
lazyenv --validate .env .env.example

# In a Makefile
check-env:
    lazyenv --validate .env .env.example
```

## Contributing

lazyenv is actively looking for contributors! Great first issues:

- [ ] Add support for additional secret key patterns
- [ ] Shell completion (bash, zsh, fish)
- [ ] Theme support (light mode)
- [ ] Integration with [Doppler](https://www.doppler.com/) / [Infisical](https://infisical.com/)
- [ ] `.env` schema definition files (type validation)
- [ ] Export to Docker `--env-file` format

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup instructions.

## Roadmap

See [ROADMAP.md](ROADMAP.md).

## License

MIT — see [LICENSE](LICENSE).

---

<p align="center">
  Made with ♥ by the lazyenv community · 
  <a href="https://github.com/ManavGurjar/lazyenv/issues">Report a bug</a> ·
  <a href="https://github.com/ManavGurjar/lazyenv/discussions">Discussions</a>
</p>

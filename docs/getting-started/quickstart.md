# Quick Start

## 1. Open your project

```bash
cd /path/to/your/project
lazyenv
```

lazyenv automatically finds all `.env*` files and opens the TUI.

## 2. Browse your files

The left sidebar lists every `.env` file found. Icons indicate health:

| Icon | Meaning |
|------|---------|
| `✓` | File is valid / matches .env.example |
| `⚠` | File has missing or mismatched keys |
| `·` | Example/sample file (reference) |

Use `↑/↓` to navigate, `Tab` to switch between the sidebar and content panel.

## 3. View key-value pairs

The main panel shows all keys and values. Secrets are masked by default (press `m` to toggle).

## 4. Check for missing keys

Press `d` to open the diff view. lazyenv automatically selects `.env.example` as the reference.

Red rows (`✗`) are keys in your example that are missing from your `.env`.

## 5. Validate in CI

```bash
# In your CI pipeline or Makefile
lazyenv --validate .env .env.example
# Exits with code 0 if valid, code 1 if keys are missing
```

## Next steps

- [TUI Interface](../guide/tui.md) — full keyboard reference
- [Diff & Validation](../guide/diff.md) — deep dive into the diff engine
- [CLI Reference](../guide/cli.md) — all command-line options
- [CI/CD Integration](../integration/ci.md) — GitHub Actions, pre-commit hooks

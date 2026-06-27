# Diff & Validation

## How diff works

lazyenv compares two `.env` files key by key and assigns each key a status:

| Status | Icon | Meaning |
|--------|------|---------|
| `OK` | (no colour) | Key exists in both files with identical values |
| `MISSING` | `✗` red | Key is in the reference (left) but absent in the current (right) |
| `EXTRA` | `+` green | Key is in the current but absent in the reference |
| `CHANGED` | `~` amber | Key exists in both but values differ |
| `EMPTY` | `·` muted | Key exists but has no value |

## In TUI mode

Press `d` to enter diff mode. lazyenv automatically selects `.env.example` (or `.env.sample`) as the reference file. The reference is shown on the left, your current `.env` on the right.

## In CLI mode

```bash
# Compare two files — exits 1 if they differ
lazyenv --diff .env .env.staging

# Validate current .env against .env.example — exits 1 if keys are missing
lazyenv --validate .env .env.example
```

## Validation vs diff

| | `--diff` | `--validate` |
|-|----------|--------------|
| Purpose | General comparison | Check completeness |
| Reference | First argument | Second argument (.env.example) |
| Exit 1 when | Any difference | MISSING keys only |
| Extra keys | Shown | Shown (but don't fail) |

## CI/CD usage

```yaml
# .github/workflows/validate-env.yml
- name: Validate environment
  run: lazyenv --validate .env.example .env.example
  # Or with a real .env populated from secrets:
  # run: lazyenv --validate .env .env.example
```

See [CI/CD Integration](../integration/ci.md) for complete examples.

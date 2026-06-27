# CLI Reference

lazyenv has a full non-interactive CLI mode for scripting and CI pipelines.

## Synopsis

```
lazyenv [OPTIONS] [PATH]
```

`PATH` defaults to the current directory.

## Options

| Option | Short | Description |
|--------|-------|-------------|
| `--version` | `-V` | Show version and exit |
| `--list` | `-l` | List all .env files found (no TUI) |
| `--diff FILE1 FILE2` | `-d` | Diff two .env files and print a table |
| `--validate ENV EXAMPLE` | `-v` | Validate ENV against EXAMPLE; exit 1 on issues |

## Examples

### List files

```bash
lazyenv --list
lazyenv --list /path/to/project
```

Output:
```
        ENV files in /my/project
┌─────────────────┬──────┬────────┐
│ File            │ Keys │ Errors │
├─────────────────┼──────┼────────┤
│ .env            │   12 │      0 │
│ .env.example    │   15 │      0 │
│ services/.env   │    8 │      0 │
└─────────────────┴──────┴────────┘
```

### Diff two files

```bash
lazyenv --diff .env .env.staging
```

Exits with code **0** if files are identical, **1** if they differ.

### Validate against example

```bash
lazyenv --validate .env .env.example
```

Exits with code **0** if all required keys are present, **1** if any are missing.

Output (failure):
```
✗ Validation failed: .env vs .env.example

  ✗ MISSING  STRIPE_SECRET_KEY
  ✗ MISSING  SENDGRID_API_KEY
```

## Environment variables

| Variable | Description |
|----------|-------------|
| `LAZYENV_MASK` | Set to `0` to disable secret masking by default |
| `LAZYENV_DEPTH` | Max directory depth to search (default: `4`) |
| `PYTHONUTF8` | Set to `1` on Windows to enable UTF-8 output |

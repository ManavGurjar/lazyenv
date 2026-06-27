# CI/CD Integration

## GitHub Actions

### Validate `.env.example` is complete

Useful for ensuring your `.env.example` stays up to date with the real env schema:

```yaml
# .github/workflows/validate-env.yml
name: Validate .env.example

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install lazyenv
      - name: Check .env.example has no empty required keys
        run: lazyenv --list  # Shows all discovered files
```

### Validate a populated .env (from secrets)

```yaml
jobs:
  validate:
    runs-on: ubuntu-latest
    env:
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
      STRIPE_SECRET_KEY: ${{ secrets.STRIPE_SECRET_KEY }}
      # ... other secrets
    steps:
      - uses: actions/checkout@v4
      - run: pip install lazyenv
      - name: Generate .env from environment
        run: env | grep -E '^[A-Z_]+=.*' > .env
      - name: Validate against .env.example
        run: lazyenv --validate .env .env.example
```

## Pre-commit hook

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: validate-env
        name: Validate .env
        entry: lazyenv --validate .env .env.example
        language: python
        additional_dependencies: [lazyenv]
        pass_filenames: false
        files: \.env
```

## Makefile

```makefile
.PHONY: check-env

check-env:
	lazyenv --validate .env .env.example

# Run before starting dev server
dev: check-env
	npm run dev
```

## Docker Compose

Add a healthcheck or startup validation:

```yaml
services:
  api:
    build: .
    command: sh -c "lazyenv --validate .env .env.example && python app.py"
    volumes:
      - .env:/app/.env:ro
      - .env.example:/app/.env.example:ro
```

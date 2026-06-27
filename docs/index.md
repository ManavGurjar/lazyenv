# lazyenv

**A beautiful TUI for managing `.env` files — like lazygit for environment variables.**

<div class="grid cards" markdown>

-   :material-magnify: **Auto-discovery**

    Finds every `.env*` file in your project, recursively. No config needed.

-   :material-eye-off: **Secrets masking**

    API keys, tokens, and passwords are masked by default. Unmask with `m`.

-   :material-compare: **Side-by-side diff**

    Press `d` to instantly see what's missing vs `.env.example`.

-   :material-console: **CLI mode**

    `lazyenv --validate .env .env.example` — CI-friendly, exits 1 on issues.

</div>

## The problem

Every developer has been here:

```
$ git clone git@github.com:company/api.git && cd api
$ cp .env.example .env
# ... 20 minutes later ...
$ Error: DATABASE_URL is not set
# ... which of the 23 keys did I miss?
```

Or worse — deployed to staging with a missing key and got a cryptic 500 error.

lazyenv fixes this with a clear, visual interface:

```
┌──────────────────────────────────────────────────────────────────────┐
│ KEY              │ REFERENCE (.env.example) │ CURRENT (.env)         │
├──────────────────┼──────────────────────────┼────────────────────────┤
│   DATABASE_URL   │ postgres://localhost/db   │ postgres://localhost/db │
│ ✗ STRIPE_KEY     │ (empty placeholder)       │ (absent)               │
│ ~ APP_PORT       │ 3000                      │ 8080                   │
│ + INTERNAL_FLAG  │ (absent)                  │ true                   │
└──────────────────┴──────────────────────────┴────────────────────────┘
  ✗ 1 missing  ~ 1 changed  + 1 extra  ✓ 8 matching
```

## Quick start

=== "pip"

    ```bash
    pip install lazyenv
    lazyenv
    ```

=== "uv"

    ```bash
    uv tool install lazyenv
    lazyenv
    ```

=== "Try without installing"

    ```bash
    uvx lazyenv
    ```

=== "Binary"

    Download from [GitHub Releases](https://github.com/lazyenv/lazyenv/releases/latest) — no Python required.

## Why developers love it

- **Zero config** — just run `lazyenv` in any project directory
- **Instant value** — the diff view alone saves hours across a team
- **CI-friendly** — `lazyenv --validate .env .env.example` in your pipeline
- **Secure by default** — secrets are masked unless you explicitly unmask them
- **Fast** — written in Python with Textual, starts in under 200ms

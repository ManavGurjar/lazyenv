# Roadmap

## v0.1.0 — MVP (current)
- [x] TUI file browser and key-value viewer
- [x] Secrets masking
- [x] Side-by-side diff
- [x] Validation against .env.example
- [x] Live search
- [x] CLI mode (`--diff`, `--validate`, `--list`)
- [x] Cross-platform (Windows, macOS, Linux)

## v0.2.0 — Shell & Editor Integration
- [ ] Shell completions (bash, zsh, fish, PowerShell)
- [ ] `lazyenv init` — scaffold a `.env.example` from your `.env`
- [ ] `lazyenv check` — alias for `--validate` with nicer output
- [ ] Git integration — warn if `.env` is accidentally staged
- [ ] Pre-commit hook: `lazyenv --validate .env .env.example`

## v0.3.0 — Schema Validation
- [ ] `.env.schema` file format (define key types, required/optional, descriptions)
- [ ] Type validation (is `PORT` actually a number? is `ENABLED` a boolean?)
- [ ] Generate `.env.example` from schema

## v0.4.0 — Team Collaboration
- [ ] Encrypted secrets with `lazyenv seal` / `lazyenv open` (similar to dotenvx)
- [ ] Export to Docker `--env-file` format
- [ ] Import from cloud providers (Doppler, Infisical, AWS SSM, Vault)
- [ ] Project switching (`lazyenv --project my-api`)

## v0.5.0 — Ecosystem Integrations
- [ ] VS Code extension
- [ ] JetBrains plugin
- [ ] GitHub Action for validating .env in CI
- [ ] Docker Compose environment validation

## Future ideas (community input welcome!)
- [ ] Web UI mode (`lazyenv serve`)
- [ ] REST API for tooling integration
- [ ] `.env` history tracking (git-based)
- [ ] Shared team templates

**Want to shape the roadmap?** Vote on or create issues at [github.com/lazyenv/lazyenv/issues](https://github.com/lazyenv/lazyenv/issues).

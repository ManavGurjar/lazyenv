# Installation

lazyenv supports Python 3.10+ and runs on Windows, macOS, and Linux.

## Package managers

=== "pip"

    ```bash
    pip install lazyenv
    ```

=== "uv (recommended)"

    ```bash
    uv tool install lazyenv
    ```

    This installs lazyenv in an isolated environment — it won't pollute your project's dependencies.

=== "pipx"

    ```bash
    pipx install lazyenv
    ```

=== "Try without installing"

    ```bash
    uvx lazyenv
    ```

## Pre-built binaries

Download a self-contained binary from the [latest release](https://github.com/lazyenv/lazyenv/releases/latest) — no Python installation required.

| Platform | File |
|----------|------|
| Linux (x64) | `lazyenv-linux-amd64` |
| macOS (x64/ARM) | `lazyenv-macos-amd64` |
| Windows (x64) | `lazyenv-windows-amd64.exe` |

```bash
# Linux / macOS
chmod +x lazyenv-linux-amd64
sudo mv lazyenv-linux-amd64 /usr/local/bin/lazyenv
```

## Verify installation

```bash
lazyenv --version
# lazyenv 0.1.0
```

## Shell aliases

lazyenv also installs a short alias `le`:

```bash
le  # same as lazyenv
```

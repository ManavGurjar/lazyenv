# Git Hooks

Integrate lazyenv into your git workflow to catch missing env vars before they cause problems.

## pre-push hook

Validate your `.env` before every push:

```bash
#!/bin/sh
# .git/hooks/pre-push
lazyenv --validate .env .env.example
if [ $? -ne 0 ]; then
    echo "❌ Fix missing env vars before pushing"
    exit 1
fi
```

Install it:

```bash
cp .git/hooks/pre-push.sample .git/hooks/pre-push
# Add the lazyenv command above
chmod +x .git/hooks/pre-push
```

## commit-msg hook

Warn (but don't block) if `.env` has issues:

```bash
#!/bin/sh
# .git/hooks/commit-msg
lazyenv --validate .env .env.example 2>/dev/null || \
    echo "⚠️  Warning: .env may have missing keys (run 'lazyenv' to check)"
```

## Using with husky (Node.js projects)

```json
// package.json
{
  "husky": {
    "hooks": {
      "pre-push": "lazyenv --validate .env .env.example"
    }
  }
}
```

## Using with lefthook

```yaml
# lefthook.yml
pre-push:
  commands:
    validate-env:
      run: lazyenv --validate .env .env.example
```

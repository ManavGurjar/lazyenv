# Launch Posts — Ready to Copy-Paste

## Hacker News — Show HN

**Title:** Show HN: lazyenv – A lazygit-style TUI for .env file management

**Body:**
```
I was tired of manually comparing .env and .env.example every time I cloned a 
repo, so I built lazyenv — a terminal UI (like lazygit) for .env files.

It auto-discovers all .env* files in your project, masks secrets by default,
and shows a live side-by-side diff against .env.example so you can instantly
see which keys are missing.

It also has a non-interactive CLI mode that's useful in CI:
  lazyenv --validate .env .env.example  (exits 1 if keys are missing)
  lazyenv init  (scaffold .env.example from .env, redacting secrets)

Zero config — just pip install lazyenv and run lazyenv in any project.

GitHub: https://github.com/ManavGurjar/lazyenv
PyPI: https://pypi.org/project/lazyenv/

Happy to hear feedback on the diff UX and what other features would be useful!
```

**Best posting time:** Monday–Wednesday, 12:00–14:00 UTC

---

## Reddit — r/Python

**Title:** I built a lazygit-style TUI for .env file management (Python + Textual)

**Body:**
```
Hey r/Python! I built lazyenv — a terminal UI for managing .env files, 
inspired by lazygit.

**The problem:** Every time I clone a repo or onboard a new teammate, someone 
inevitably misses a key in .env.example. Then they get a cryptic error 30 
minutes into their setup.

**What lazyenv does:**
- Auto-discovers all .env* files in your project
- Masks secrets by default (toggle with `m`)
- Side-by-side diff against .env.example (`d` key)
- Live search/filter (`/` key)
- `lazyenv --validate .env .env.example` for CI pipelines
- `lazyenv init` to scaffold .env.example from .env

Built with Python + Textual (which is an amazing TUI framework — 
highly recommend checking it out).

GitHub: https://github.com/ManavGurjar/lazyenv
Install: pip install lazyenv (or uvx lazyenv to try without installing)

Would love feedback, especially on what's missing for your workflow!
```

---

## Reddit — r/devops

**Title:** CLI tool to validate .env files in CI — lazyenv --validate

**Body:**
```
Quick share: I added a --validate flag to lazyenv (a .env file manager) 
that's useful for CI pipelines:

  pip install lazyenv
  lazyenv --validate .env .env.example
  # Exits 0 if valid, exits 1 if keys are missing

Works great as a pre-push hook or in GitHub Actions before deploying.

Also has a full TUI mode for interactive browsing/diffing during development.

https://github.com/ManavGurjar/lazyenv
```

---

## X (Twitter) — Thread

**Tweet 1 (with GIF):**
```
Stop losing hours to missing .env keys.

Meet lazyenv — a lazygit-style TUI for your .env files.

✓ Auto-discovers all .env* files
✓ Secrets masked by default  
✓ Side-by-side diff vs .env.example
✓ `pip install lazyenv`

[GIF HERE]

github.com/ManavGurjar/lazyenv
```

**Tweet 2:**
```
The diff view alone is worth it.

Press `d` in lazyenv → instantly see:
• ✗ missing keys (red)
• ~ changed values (amber)  
• + extra keys (green)

No more "why isn't this working in staging" mysteries.
```

**Tweet 3:**
```
Also works in CI:

  lazyenv --validate .env .env.example

Exits 1 if any required keys are missing. 

Add it to your Makefile, pre-commit hook, or GitHub Actions pipeline.
```

---

## Dev.to Article

**Title:** I built a lazygit-style TUI for .env files — and here's what I learned about Textual

**Outline:**
1. The problem (missing env vars, manual comparison)
2. Why I chose Textual (Python TUI framework)
3. Building the parser (quoted values, secrets detection)
4. The diff engine (key-by-key comparison)
5. What I'd do differently (Go for faster startup)
6. Demo / install instructions

---

## Product Hunt

**Tagline:** A beautiful TUI for managing .env files — like lazygit for environment variables

**Description:**
lazyenv is a terminal UI (like lazygit) that makes .env file management visual
and effortless. It auto-discovers all .env* files in your project, masks 
secrets by default, and shows a live side-by-side diff against .env.example.

Perfect for: onboarding new teammates, catching missing env vars before deploy,
and keeping your dev/staging/prod environments in sync.

**Links:**
- GitHub: https://github.com/ManavGurjar/lazyenv  
- Install: pip install lazyenv
- Docs: https://ManavGurjar.github.io/lazyenv

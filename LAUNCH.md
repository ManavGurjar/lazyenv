# lazyenv Launch Strategy

## Target: 5,000 GitHub stars in 6 months

---

## Why this will work

lazyenv targets **every developer** (not a niche) with a problem they encounter **multiple times per day**. The value proposition fits in one sentence:

> *"lazygit for your .env files — browse, compare, and validate across your whole project."*

---

## Week 1: Launch

### Day 0 (pre-launch)
- [ ] Create GitHub org: `lazyenv`
- [ ] Push repo with all files (including the GIF below)
- [ ] Create PyPI account and publish `lazyenv 0.1.0`
- [ ] Record a 60-second terminal screen recording showing:
  1. `pip install lazyenv && lazyenv` — zero config
  2. Browse files in sidebar
  3. Press `d` — diff view reveals 3 missing keys
  4. Press `/` — live filter
  5. Press `m` — unmask a secret
- [ ] Convert recording to GIF and embed in README

### Day 1: Show HN
Post between **12:00–14:00 UTC** on a weekday.

Title: **"Show HN: lazyenv – A lazygit-style TUI for .env files"**

Body:
```
I got tired of manually comparing .env and .env.example every time I 
cloned a repo, so I built lazyenv.

It's a terminal UI (like lazygit) that:
- Auto-discovers all .env* files in your project
- Masks secrets by default
- Shows a live side-by-side diff against .env.example
- Works as a CI validator: lazyenv --validate .env .env.example (exits 1 if keys are missing)

Zero config. Works on macOS, Linux, Windows.

pip install lazyenv (or uvx lazyenv to try without installing)

GitHub: https://github.com/lazyenv/lazyenv
```

### Day 2: Reddit
- r/Python: "I built a lazygit-style TUI for .env file management"
- r/programming: same post
- r/webdev: "Stop manually checking which env vars are missing"
- r/devops: "One command to validate your .env against .env.example in CI"

### Day 3: Social
- X/Twitter: Demo GIF + short thread
  - Tweet 1: GIF + "Stop losing hours to missing env vars. Meet lazyenv."
  - Tweet 2: "The diff view that saves you from 'why isn't this working in staging'"
  - Tweet 3: "Works in CI too: `lazyenv --validate .env .env.example`"
- LinkedIn post
- Mastodon / Fosstodon

### Day 4-7: Content
- Dev.to article: "I built a TUI for .env files and here's what I learned"
- Hashnode: cross-post
- Personal blog post (if applicable)

---

## Month 1: Community building

### Features that attract contributors
1. **"good first issue" labels** on easy wins:
   - Add secret key patterns (low barrier, anyone can contribute)
   - Shell completions
   - More test coverage
2. **Well-documented extension points** — easy to add new parsers
3. **Respond to issues within 24 hours** — reputation for responsiveness attracts contributors

### SEO + discoverability
- Ensure README has keywords: dotenv, env, environment variables, .env viewer, env manager
- Add GitHub topics: `dotenv` `env` `tui` `cli` `developer-tools` `python` `textual`

---

## Month 2-3: Ecosystem integration

### Integrations that generate press
- **Pre-commit hook**: `lazyenv --validate .env .env.example`
- **GitHub Action**: validate .env in CI/CD workflows
- **VS Code extension**: show .env health in status bar

### Community partnerships
- Reach out to: Textual team (Charm-equivalent), dotenvx, mise
- Guest post on their blogs: "Building a TUI with Textual"
- Mention in Python Weekly, PyCoder's Weekly newsletters

---

## Month 4-6: Sustaining momentum

### Weekly release cadence
Ship something every 1-2 weeks:
- v0.2: Shell completions + `lazyenv init`
- v0.3: Schema validation (`.env.schema` format)
- v0.4: Encrypted secrets
- v0.5: Doppler/Infisical import

### Content flywheel
- Each release = a Show HN / Reddit post
- Each integration = a blog post
- Monthly "What's new in lazyenv" newsletter/post

---

## KPI targets

| Metric | Week 1 | Month 1 | Month 3 | Month 6 |
|--------|--------|---------|---------|---------|
| GitHub stars | 500 | 1,000 | 2,500 | 5,000 |
| PyPI downloads/month | 200 | 1,000 | 5,000 | 15,000 |
| Contributors | 0 | 3 | 10 | 25 |
| Issues/PRs | 5 | 20 | 60 | 150 |

---

## The demo GIF is critical

The single highest-impact action: a beautiful, 15-second GIF that shows:
1. Cold terminal, type `lazyenv`
2. Beautiful TUI appears instantly
3. Press `d` — diff view animates in showing missing keys in red
4. Press `m` — secrets unmask

This GIF will be shared independently of the README. People share "wow" demos.

Record with: `vhs` (by Charm) or `asciinema` → `svg-term`.

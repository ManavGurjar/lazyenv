# TUI Interface

## Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│ lazyenv                                              12:34:56        │  ← Header
├─────────────────────┬────────────────────────────────────────────────┤
│ 📁 ENV FILES        │  KEY                 = VALUE                   │
│                     │                                                │  ← Content
│ ✓ .env              │  # Database                                    │     panel
│ ⚠ .env.local        │  DATABASE_URL        = postgres://localhost/db  │
│ · .env.example      │  DB_PASSWORD         = ••••••••••••            │
│ ✓ services/api/.env │                                                │
│                     │  # API Keys                                    │
│                     │  STRIPE_SECRET_KEY   = ••••••••••••            │
│  ↑↓ navigate        │  OPENAI_API_KEY      = ••••••••••••            │
│  Enter select       │                                                │
│                     │  # App config                                  │
│                     │  APP_ENV             = development             │
│                     │  APP_PORT            = 3000                    │
├─────────────────────┴────────────────────────────────────────────────┤
│ lazyenv  .env  │  4 files  │  MASK ON                               │  ← Status
│  q Quit  d Diff  m Mask  c Copy  e Edit  / Filter  ? Help           │  ← Footer
└──────────────────────────────────────────────────────────────────────┘
```

## File list (left panel)

| Icon | Meaning |
|------|---------|
| `✓` | All keys match `.env.example` |
| `⚠` | Has missing or extra keys vs `.env.example` |
| `·` | Example/sample reference file |

## Content panel (right)

Shows all entries in the selected `.env` file:

- **Comment lines** appear in muted italic (`# Database`)
- **Keys** appear in blue bold
- **Values** — masked if the key name matches a secret pattern
- **Empty values** shown as `(empty)` in italic

## Diff mode

Press `d` to toggle. The layout changes to a three-column view:

```
KEY              │ REFERENCE (.env.example) │ CURRENT (.env)
─────────────────┼──────────────────────────┼────────────────
DATABASE_URL     │ postgres://localhost/db   │ postgres://loc…
✗ STRIPE_KEY     │ (empty placeholder)       │ (absent)
~ APP_PORT       │ 3000                      │ 8080
+ INTERNAL_FLAG  │ (absent)                  │ true
```

Row colours:
- **Red** — key is in the reference but missing from current
- **Amber** — key exists in both but values differ
- **Green** — key is in current but not in reference (extra)
- **No colour** — key matches

## Search / filter

Press `/` or `f` to open the search bar. Type to filter keys in real time. Press `Esc` to clear.

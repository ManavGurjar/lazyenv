"""Help screen."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import ModalScreen
from textual.widgets import Markdown

_HELP_MD = """\
# lazyenv — Keyboard Reference

## Navigation
| Key | Action |
|-----|--------|
| `Tab` | Switch between file list and content panel |
| `↑/↓` | Move selection |
| `Enter` | Select file |
| `q` | Quit |

## Viewing
| Key | Action |
|-----|--------|
| `m` | Toggle secret masking |
| `/` or `f` | Filter keys |
| `Esc` | Clear filter |
| `c` | Copy selected value to clipboard |

## Diff
| Key | Action |
|-----|--------|
| `d` | Toggle diff view (compares against .env.example) |

## File
| Key | Action |
|-----|--------|
| `e` | Open file in $EDITOR |
| `r` / `Ctrl+R` | Reload all files |
| `?` | Show this help |

---
*lazyenv* — [https://github.com/lazyenv/lazyenv](https://github.com/lazyenv/lazyenv)
"""


class HelpScreen(ModalScreen[None]):
    """Full-screen help overlay."""

    DEFAULT_CSS = """
    HelpScreen {
        align: center middle;
    }
    HelpScreen > Markdown {
        width: 70;
        max-height: 35;
        background: #1e1e2e;
        border: solid #7c3aed;
        padding: 1 2;
    }
    """

    BINDINGS = [
        Binding("escape", "dismiss", "Close"),
        Binding("q", "dismiss", "Close"),
        Binding("?", "dismiss", "Close"),
    ]

    def compose(self) -> ComposeResult:
        yield Markdown(_HELP_MD)

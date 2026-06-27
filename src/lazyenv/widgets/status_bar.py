"""Bottom status bar widget."""

from __future__ import annotations

from pathlib import Path

from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Label


class StatusBar(Widget):
    """One-line status bar showing context."""

    DEFAULT_CSS = """
    StatusBar {
        height: 1;
        background: #5b21b6;
        layout: horizontal;
        padding: 0 1;
    }
    StatusBar Label { color: white; margin-right: 2; }
    StatusBar .badge { background: #7c3aed; padding: 0 1; margin-right: 1; }
    StatusBar .badge-on { background: #10b981; color: #1e1e2e; text-style: bold; padding: 0 1; }
    StatusBar .badge-off { background: #374151; color: #9ca3af; padding: 0 1; }
    StatusBar .path { color: #c4b5fd; }
    StatusBar .sep { color: #7c3aed; margin: 0 1; }
    """

    def compose(self) -> ComposeResult:
        yield Label("lazyenv", classes="badge")
        yield Label("", id="sb-path", classes="path")
        yield Label("│", classes="sep")
        yield Label("", id="sb-count")
        yield Label("│", classes="sep")
        yield Label("", id="sb-mask", classes="badge-off")
        yield Label("", id="sb-diff", classes="badge-off")

    def update(
        self,
        file_count: int,
        current_file: Path | None,
        mask_on: bool,
        diff_on: bool,
        root: Path,
    ) -> None:
        if current_file:
            try:
                rel = current_file.relative_to(root)
            except ValueError:
                rel = current_file
            self.query_one("#sb-path", Label).update(str(rel))
        self.query_one("#sb-count", Label).update(f"{file_count} file{'s' if file_count != 1 else ''}")

        mask_lbl = self.query_one("#sb-mask", Label)
        mask_lbl.update("MASK ON" if mask_on else "MASK OFF")
        mask_lbl.set_class(mask_on, "badge-on")
        mask_lbl.set_class(not mask_on, "badge-off")

        diff_lbl = self.query_one("#sb-diff", Label)
        diff_lbl.update("DIFF" if diff_on else "")
        diff_lbl.set_class(diff_on, "badge-on")
        diff_lbl.set_class(not diff_on, "badge-off")

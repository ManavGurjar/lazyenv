"""Side-by-side diff widget."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import ScrollableContainer, Vertical
from textual.widget import Widget
from textual.widgets import Label, Static

from lazyenv.models import DiffEntry, EnvDiff, EntryStatus

_STATUS_ICON = {
    EntryStatus.OK: "  ",
    EntryStatus.MISSING: "✗ ",
    EntryStatus.EXTRA: "+ ",
    EntryStatus.CHANGED: "~ ",
    EntryStatus.EMPTY: "· ",
}

_STATUS_CLASS = {
    EntryStatus.OK: "status-ok",
    EntryStatus.MISSING: "status-missing",
    EntryStatus.EXTRA: "status-extra",
    EntryStatus.CHANGED: "status-changed",
    EntryStatus.EMPTY: "status-empty",
}


class DiffRow(Widget):
    DEFAULT_CSS = """
    DiffRow { height: 1; layout: horizontal; }
    DiffRow .dk { width: 26; padding: 0 1; text-style: bold; }
    DiffRow .dl { width: 1fr; padding: 0 1; border-left: solid #5b21b6; overflow: hidden; }
    DiffRow .dr { width: 1fr; padding: 0 1; border-left: solid #5b21b6; overflow: hidden; }
    DiffRow.row-missing { background: #991b1b 25%; }
    DiffRow.row-extra   { background: #166534 25%; }
    DiffRow.row-changed { background: #92400e 25%; }
    """

    def __init__(self, entry: DiffEntry, mask: bool) -> None:
        row_cls = f"row-{entry.status.value}" if entry.status != EntryStatus.OK else ""
        super().__init__(classes=row_cls)
        self.entry = entry
        self.mask = mask

    def compose(self) -> ComposeResult:
        status_cls = _STATUS_CLASS[self.entry.status]
        icon = _STATUS_ICON[self.entry.status]

        def _display(val: str, is_secret: bool) -> str:
            if not val:
                return "(empty)"
            if self.mask and is_secret:
                return "•" * min(len(val), 16)
            return val

        is_secret = bool(
            self.entry.left_entry and self.entry.left_entry.masked
            or self.entry.right_entry and self.entry.right_entry.masked
        )

        left_val = _display(self.entry.left_value, is_secret)
        right_val = _display(self.entry.right_value, is_secret)

        yield Label(f"{icon}{self.entry.key[:24]}", classes=f"dk {status_cls}")
        yield Label(left_val, classes="dl")
        yield Label(right_val, classes="dr")


class DiffView(Widget):
    """Full side-by-side diff view."""

    DEFAULT_CSS = """
    DiffView { height: 1fr; }
    DiffView .diff-header { height: 1; layout: horizontal; background: #313244; }
    DiffView .dh-icon { width: 26; padding: 0 1; color: #6b7280; }
    DiffView .dh-left { width: 1fr; padding: 0 1; border-left: solid #5b21b6; color: #93c5fd; text-style: bold; }
    DiffView .dh-right { width: 1fr; padding: 0 1; border-left: solid #5b21b6; color: #86efac; text-style: bold; }
    DiffView .diff-summary { height: 1; background: #313244; border-top: solid #5b21b6; padding: 0 1; color: #6b7280; }
    """

    def compose(self) -> ComposeResult:
        with Vertical():
            with Widget(classes="diff-header"):
                yield Label("KEY", classes="dh-icon")
                yield Label("REFERENCE (.env.example)", classes="dh-left")
                yield Label("CURRENT (.env)", classes="dh-right")
            yield ScrollableContainer(id="diff-scroll")
            yield Static("", id="diff-summary", classes="diff-summary")

    def load_diff(self, diff: EnvDiff, mask: bool = True) -> None:
        scroll = self.query_one("#diff-scroll", ScrollableContainer)
        scroll.remove_children()

        rows = [DiffRow(entry, mask=mask) for entry in diff.entries]
        if rows:
            scroll.mount(*rows)

        summary = self.query_one("#diff-summary", Static)
        parts = []
        if diff.missing_count:
            parts.append(f"[red]✗ {diff.missing_count} missing[/red]")
        if diff.extra_count:
            parts.append(f"[green]+ {diff.extra_count} extra[/green]")
        if diff.changed_count:
            parts.append(f"[yellow]~ {diff.changed_count} changed[/yellow]")
        if diff.ok_count:
            parts.append(f"[dim]{diff.ok_count} matching[/dim]")
        summary.update("  ".join(parts) if parts else "[green]✓ Files are in sync[/green]")

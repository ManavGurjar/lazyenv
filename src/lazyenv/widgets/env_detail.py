"""Env detail panel — scrollable key-value viewer with search and copy."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import ScrollableContainer, Vertical
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Input, Label, Static

from lazyenv.models import EnvEntry, EnvFile


class EntryRow(Widget):
    """A single key=value row."""

    DEFAULT_CSS = """
    EntryRow {
        height: 1;
        layout: horizontal;
        padding: 0 1;
    }
    EntryRow:hover { background: #7c3aed 20%; }
    EntryRow.selected { background: #7c3aed 40%; }
    EntryRow .key { width: 28; color: #93c5fd; text-style: bold; overflow: hidden; }
    EntryRow .eq  { width: 3; color: #6b7280; }
    EntryRow .val { width: 1fr; overflow: hidden; }
    EntryRow .val--masked { color: #6b7280; }
    EntryRow .val--empty  { color: #6b7280; text-style: italic; }
    """

    BINDINGS = [Binding("enter", "select", "Select", show=False)]

    def __init__(self, entry: EnvEntry, mask: bool, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.entry = entry
        self.mask = mask
        self.can_focus = True

    def compose(self) -> ComposeResult:
        yield Label(self.entry.key[:27], classes="key")
        yield Label(" = ", classes="eq")
        val_cls = "val"
        if self.mask and self.entry.masked:
            val_cls += " val--masked"
            display = "•" * min(len(self.entry.value), 16) if self.entry.value else "(empty)"
        elif self.entry.is_empty:
            val_cls += " val--empty"
            display = "(empty)"
        else:
            display = self.entry.value
        yield Label(display, classes=val_cls)

    def action_select(self) -> None:
        self.add_class("selected")

    @property
    def copyable_value(self) -> str:
        return self.entry.value


class CommentRow(Static):
    DEFAULT_CSS = "CommentRow { height: 1; padding: 0 1; color: #6b7280; text-style: italic; }"


class EnvDetail(Widget):
    """Main content panel displaying all entries of the selected file."""

    _file: EnvFile | None = None
    _mask: bool = True
    _filter: str = ""
    _selected_idx: int = -1

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Input(placeholder="/ to filter keys…", id="search-input")
            yield ScrollableContainer(id="entry-scroll")

    def on_mount(self) -> None:
        self.query_one("#search-input").display = False

    def load_file(self, file: EnvFile, mask: bool = True) -> None:
        self._file = file
        self._mask = mask
        self._filter = ""
        self._rebuild()
        # reset search bar
        inp = self.query_one("#search-input", Input)
        inp.value = ""
        inp.display = False

    def _rebuild(self) -> None:
        scroll = self.query_one("#entry-scroll", ScrollableContainer)
        scroll.remove_children()
        if not self._file:
            return

        query = self._filter.lower()
        rows: list[Widget] = []
        for entry in self._file.entries:
            if entry.is_blank:
                rows.append(Static("", classes="blank-line"))
                continue
            if entry.is_comment_line:
                rows.append(CommentRow(f"# {entry.comment}"))
                continue
            if query and query not in entry.key.lower() and query not in entry.value.lower():
                continue
            rows.append(EntryRow(entry, mask=self._mask))

        scroll.mount(*rows)

    def focus_search(self) -> None:
        inp = self.query_one("#search-input", Input)
        inp.display = True
        inp.focus()

    def clear_search(self) -> None:
        inp = self.query_one("#search-input", Input)
        self._filter = ""
        inp.value = ""
        inp.display = False
        self._rebuild()

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "search-input":
            self._filter = event.value
            self._rebuild()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "search-input":
            rows = self.query(EntryRow)
            if rows:
                rows.first().focus()

    def copy_selected(self) -> str | None:
        focused = self.query("EntryRow:focus")
        if focused:
            return focused.first(EntryRow).copyable_value
        # fallback: first row
        rows = self.query(EntryRow)
        if rows:
            return rows.first().copyable_value
        return None

    def focus(self) -> "EnvDetail":
        rows = self.query(EntryRow)
        if rows:
            rows.first().focus()
        return self

"""Sidebar file list widget."""

from __future__ import annotations

from pathlib import Path

from textual.app import ComposeResult
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Label, ListItem, ListView

from lazyenv.diff import validate_against_example
from lazyenv.models import EnvFile


class FileList(Widget):
    """Left-panel file browser."""

    DEFAULT_CSS = ""

    class FileSelected(Message):
        def __init__(self, env_file: EnvFile) -> None:
            super().__init__()
            self.env_file = env_file

    _files: list[EnvFile] = []
    _root: Path | None = None

    def compose(self) -> ComposeResult:
        yield Label(" 📁 ENV FILES", classes="header")
        yield ListView(id="file-listview")

    def update_files(self, files: list[EnvFile], root: Path) -> None:
        self._files = files
        self._root = root
        lv = self.query_one(ListView)
        lv.clear()

        example_files = [f for f in files if "example" in f.name or "sample" in f.name]
        example_paths = {f.path for f in example_files}

        def _item_class(f: EnvFile) -> str:
            if f.path in example_paths:
                return "file-item--example"
            # check for issues against example
            ex = next((e for e in example_files if e.path.parent == f.path.parent), None)
            if ex:
                d = validate_against_example(f, ex)
                if d.has_issues:
                    return "file-item--has-issues"
            return "file-item--ok"

        for f in files:
            try:
                rel = f.path.relative_to(root) if root else f.path
            except ValueError:
                rel = f.path
            cls = _item_class(f)
            icon = "⚠ " if cls == "file-item--has-issues" else ("· " if cls == "file-item--example" else "✓ ")
            item = ListItem(Label(f"{icon}{rel}"), classes=cls)
            item._env_file = f  # type: ignore[attr-defined]
            lv.append(item)

        if lv._nodes:
            lv.index = 0

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item = event.item
        env_file: EnvFile | None = getattr(item, "_env_file", None)
        if env_file:
            self.post_message(self.FileSelected(env_file))

    def focus(self) -> FileList:
        self.query_one(ListView).focus()
        return self

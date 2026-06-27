"""Main Textual application for lazyenv."""

from __future__ import annotations

from pathlib import Path

from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import Footer, Header, Label, ListItem, ListView, Static

from lazyenv.diff import diff_files, validate_against_example
from lazyenv.models import EnvDiff, EnvFile
from lazyenv.parser import parse_directory, parse_file
from lazyenv.widgets.diff_view import DiffView
from lazyenv.widgets.env_detail import EnvDetail
from lazyenv.widgets.file_list import FileList
from lazyenv.widgets.status_bar import StatusBar


class LazyEnv(App[None]):
    """lazyenv — a beautiful TUI for managing .env files."""

    TITLE = "lazyenv"
    CSS_PATH = "styles/main.tcss"
    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("?", "help", "Help"),
        Binding("r", "reload", "Reload"),
        Binding("d", "toggle_diff", "Diff"),
        Binding("m", "toggle_mask", "Mask secrets"),
        Binding("c", "copy_value", "Copy"),
        Binding("e", "open_editor", "Edit"),
        Binding("f", "focus_filter", "Filter", key_display="/"),
        Binding("/", "focus_filter", "Filter", show=False),
        Binding("tab", "switch_panel", "Switch panel"),
        Binding("escape", "escape", "Back", show=False),
        Binding("ctrl+r", "reload", "Reload", show=False),
    ]

    # State
    root_path: Path
    env_files: reactive[list[EnvFile]] = reactive([], recompose=False)
    selected_file: reactive[EnvFile | None] = reactive(None)
    compare_file: reactive[EnvFile | None] = reactive(None)
    mask_secrets: reactive[bool] = reactive(True)
    diff_mode: reactive[bool] = reactive(False)

    def __init__(self, root: Path) -> None:
        super().__init__()
        self.root_path = root.resolve()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="main"):
            yield FileList(id="file-list")
            with Vertical(id="content-area"):
                yield EnvDetail(id="env-detail")
                yield DiffView(id="diff-view")
        yield StatusBar(id="status-bar")
        yield Footer()

    def on_mount(self) -> None:
        self.load_files()
        self.query_one(DiffView).display = False

    @work(thread=True)
    def load_files(self) -> None:
        files = parse_directory(self.root_path)
        self.call_from_thread(self._set_files, files)

    def _set_files(self, files: list[EnvFile]) -> None:
        self.env_files = files
        file_list = self.query_one(FileList)
        file_list.update_files(files, self.root_path)
        if files:
            self.selected_file = files[0]
        self._update_status()

    def watch_selected_file(self, file: EnvFile | None) -> None:
        if file is None:
            return
        detail = self.query_one(EnvDetail)
        detail.load_file(file, mask=self.mask_secrets)
        if self.diff_mode and self.compare_file:
            self._refresh_diff()

    def watch_mask_secrets(self, mask: bool) -> None:
        if self.selected_file:
            self.query_one(EnvDetail).load_file(self.selected_file, mask=mask)
        self._update_status()

    def watch_diff_mode(self, active: bool) -> None:
        diff_view = self.query_one(DiffView)
        env_detail = self.query_one(EnvDetail)
        if active:
            env_detail.display = False
            diff_view.display = True
            self._refresh_diff()
        else:
            diff_view.display = False
            env_detail.display = True
        self._update_status()

    def _refresh_diff(self) -> None:
        if not self.selected_file:
            return
        compare = self.compare_file or self._find_example_for(self.selected_file)
        if compare:
            env_diff = validate_against_example(self.selected_file, compare)
        else:
            # Self-diff placeholder
            env_diff = diff_files(self.selected_file, self.selected_file)
        self.query_one(DiffView).load_diff(
            env_diff, mask=self.mask_secrets
        )

    def _find_example_for(self, env: EnvFile) -> EnvFile | None:
        """Auto-select .env.example or .env.sample as the reference."""
        for f in self.env_files:
            if "example" in f.name or "sample" in f.name:
                return f
        return None

    def _update_status(self) -> None:
        bar = self.query_one(StatusBar)
        count = len(self.env_files)
        sel = self.selected_file
        bar.update(
            file_count=count,
            current_file=sel.path if sel else None,
            mask_on=self.mask_secrets,
            diff_on=self.diff_mode,
            root=self.root_path,
        )

    # ── Actions ────────────────────────────────────────────────────────────

    def action_reload(self) -> None:
        self.notify("Reloading files…", title="lazyenv")
        self.load_files()

    def action_toggle_diff(self) -> None:
        self.diff_mode = not self.diff_mode

    def action_toggle_mask(self) -> None:
        self.mask_secrets = not self.mask_secrets

    def action_copy_value(self) -> None:
        detail = self.query_one(EnvDetail)
        copied = detail.copy_selected()
        if copied:
            self.notify(f"Copied: {copied[:40]}…" if len(copied) > 40 else f"Copied: {copied}")

    def action_focus_filter(self) -> None:
        self.query_one(EnvDetail).focus_search()

    def action_switch_panel(self) -> None:
        file_list = self.query_one(FileList)
        detail = self.query_one(EnvDetail)
        if file_list.has_focus or any(w.has_focus for w in file_list.query("*")):
            detail.focus()
        else:
            file_list.focus()

    def action_escape(self) -> None:
        self.query_one(EnvDetail).clear_search()

    def action_open_editor(self) -> None:
        if self.selected_file:
            import os
            import subprocess
            editor = os.environ.get("EDITOR", "notepad" if os.name == "nt" else "nano")
            self.suspend()
            try:
                subprocess.run([editor, str(self.selected_file.path)])
            finally:
                self.resume()
            self.load_files()

    def action_help(self) -> None:
        from lazyenv.screens.help import HelpScreen
        self.push_screen(HelpScreen())

    # ── Events ─────────────────────────────────────────────────────────────

    @on(FileList.FileSelected)
    def on_file_selected(self, event: FileList.FileSelected) -> None:
        self.selected_file = event.env_file
        if self.diff_mode:
            self._refresh_diff()

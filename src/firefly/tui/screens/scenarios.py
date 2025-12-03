"""Scenarios screen - save/load scenarios."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static


class ScenariosScreen(Screen):
    """Scenarios screen for saving/loading."""

    def compose(self) -> ComposeResult:
        yield Static("Scenarios - Coming Soon")

"""Comparison screen - compare multiple scenarios."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static


class ComparisonScreen(Screen):
    """Comparison screen for multiple scenarios."""

    def compose(self) -> ComposeResult:
        yield Static("Comparison Mode - Coming Soon")

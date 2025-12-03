"""Settings screen - app configuration."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static


class SettingsScreen(Screen):
    """Settings screen for configuration."""

    def compose(self) -> ComposeResult:
        yield Static("Settings - Coming Soon")

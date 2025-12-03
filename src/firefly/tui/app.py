"""Main Textual application for Firefly TUI."""

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, TabbedContent, TabPane

from firefly.tui.screens.calculator import CalculatorScreen
from firefly.tui.screens.comparison import ComparisonScreen
from firefly.tui.screens.scenarios import ScenariosScreen
from firefly.tui.screens.settings import SettingsScreen


class FireflyApp(App):
    """Firefly TUI application with tabbed interface."""

    CSS = """
    Screen {
        background: $surface;
    }

    TabbedContent {
        height: 1fr;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("?", "help", "Help"),
        ("S", "save", "Save"),
        ("L", "load", "Load"),
        ("C", "compare", "Compare"),
        ("R", "reset", "Reset"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()

        with TabbedContent(initial="calculator"):
            with TabPane("Calculator", id="calculator"):
                yield CalculatorScreen()
            with TabPane("Comparison", id="comparison"):
                yield ComparisonScreen()
            with TabPane("Scenarios", id="scenarios"):
                yield ScenariosScreen()
            with TabPane("Settings", id="settings"):
                yield SettingsScreen()

        yield Footer()

    def action_save(self) -> None:
        """Save current scenario."""
        self.notify("Saving scenario...")

    def action_load(self) -> None:
        """Load a scenario."""
        self.notify("Loading scenario...")

    def action_compare(self) -> None:
        """Switch to comparison tab."""
        self.query_one(TabbedContent).active = "comparison"

    def action_reset(self) -> None:
        """Reset current inputs to defaults."""
        self.notify("Resetting to defaults...")

    def action_help(self) -> None:
        """Show help overlay."""
        self.notify("Help: q=Quit | S=Save | L=Load | C=Compare | R=Reset | Tab=Navigate")


def main():
    """Entry point for Firefly TUI."""
    app = FireflyApp()
    app.run()

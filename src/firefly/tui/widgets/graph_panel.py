"""Graph panel widget displaying portfolio growth."""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from firefly.core.models.compound_interest import CompoundInterestResult
from firefly.tui.utils.graphing import generate_ascii_graph


class GraphPanel(Vertical):
    """Right panel displaying live graph."""

    CSS = """
    GraphPanel {
        padding: 1 2;
    }

    .title {
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
    }

    .graph {
        height: 1fr;
        overflow: auto;
    }
    """

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Static("Portfolio Growth", classes="title")
        yield Static("", id="graph_display", classes="graph")

    def update_graph(self, result: CompoundInterestResult) -> None:
        """Update graph with new calculation result."""
        graph_text = generate_ascii_graph(result)
        graph_display = self.query_one("#graph_display", Static)
        graph_display.update(graph_text)

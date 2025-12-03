"""Stats bar widget showing summary statistics."""

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static

from firefly.core.models.compound_interest import CompoundInterestResult


class StatsBar(Horizontal):
    """Bottom bar displaying key statistics."""

    CSS = """
    StatsBar {
        background: $boost;
        height: 3;
        align: center middle;
    }

    Static {
        margin: 0 2;
        text-style: bold;
    }

    .stat-value {
        color: $success;
    }
    """

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Static("Final: $0", id="final_stat")
        yield Static("Contributions: $0", id="contrib_stat")
        yield Static("Interest: $0", id="interest_stat")
        yield Static("ROI: 0%", id="roi_stat")

    def update_stats(self, result: CompoundInterestResult) -> None:
        """Update statistics with new calculation result."""
        final = self.query_one("#final_stat", Static)
        contrib = self.query_one("#contrib_stat", Static)
        interest = self.query_one("#interest_stat", Static)
        roi = self.query_one("#roi_stat", Static)

        # Calculate ROI
        total_invested = result.input_params.principal + result.total_contributions
        roi_percent = (result.total_interest / total_invested * 100) if total_invested > 0 else 0

        # Update displays
        final.update(f"Final: ${result.final_amount:,.2f}")
        contrib.update(f"Contributions: ${result.total_contributions:,.2f}")
        interest.update(f"Interest: ${result.total_interest:,.2f}")
        roi.update(f"ROI: {roi_percent:.1f}%")

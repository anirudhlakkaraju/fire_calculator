"""Calculator screen - main tab for compound interest calculations."""

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.screen import Screen

from firefly.core.calculators.compound_interest import CompoundInterestCalculator
from firefly.core.models.compound_interest import CompoundingFrequency, CompoundInterestInput
from firefly.tui.widgets.graph_panel import GraphPanel
from firefly.tui.widgets.input_panel import InputPanel
from firefly.tui.widgets.stats_bar import StatsBar


class CalculatorScreen(Screen):
    """Main calculator screen with split layout."""

    CSS = """
    CalculatorScreen {
        layout: vertical;
    }

    Horizontal {
        height: 1fr;
    }

    InputPanel {
        width: 40%;
        border: solid $primary;
    }

    GraphPanel {
        width: 60%;
        border: solid $accent;
    }

    StatsBar {
        height: 3;
        dock: bottom;
    }
    """

    # Reactive state for calculator inputs
    principal = reactive(10000.0)
    annual_rate = reactive(7.0)
    years = reactive(10)
    months = reactive(0)
    monthly_contribution = reactive(0.0)
    annual_contribution = reactive(0.0)
    compounding_frequency = reactive(CompoundingFrequency.ANNUALLY)

    def __init__(self):
        super().__init__()
        self.calculator = CompoundInterestCalculator()
        self.result = None

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        with Horizontal():
            yield InputPanel(id="input_panel")
            yield GraphPanel(id="graph_panel")
        yield StatsBar(id="stats_bar")

    def on_mount(self) -> None:
        """Called when screen is mounted."""
        self.calculate()

    def watch_principal(self, value: float) -> None:
        """React to principal changes."""
        self.calculate()

    def watch_annual_rate(self, value: float) -> None:
        """React to rate changes."""
        self.calculate()

    def watch_years(self, value: int) -> None:
        """React to years changes."""
        self.calculate()

    def watch_months(self, value: int) -> None:
        """React to months changes."""
        self.calculate()

    def watch_monthly_contribution(self, value: float) -> None:
        """React to monthly contribution changes."""
        self.calculate()

    def watch_annual_contribution(self, value: float) -> None:
        """React to annual contribution changes."""
        self.calculate()

    def watch_compounding_frequency(self, value: CompoundingFrequency) -> None:
        """React to compounding frequency changes."""
        self.calculate()

    def calculate(self) -> None:
        """Calculate and update display."""
        params = CompoundInterestInput(
            principal=self.principal,
            annual_rate=self.annual_rate,
            years=self.years,
            months=self.months,
            monthly_contribution=self.monthly_contribution,
            annual_contribution=self.annual_contribution,
            compounding_frequency=self.compounding_frequency,
        )

        self.result = self.calculator.calculate(params)

        # Update graph and stats
        graph_panel = self.query_one("#graph_panel", GraphPanel)
        stats_bar = self.query_one("#stats_bar", StatsBar)

        graph_panel.update_graph(self.result)
        stats_bar.update_stats(self.result)

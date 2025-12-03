"""Input panel widget with form fields."""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Input, Label, Select, Static

from firefly.core.models.compound_interest import CompoundingFrequency


class InputPanel(Vertical):
    """Left panel containing input fields."""

    CSS = """
    InputPanel {
        padding: 1 2;
    }

    Label {
        margin-top: 1;
        color: $text-muted;
    }

    Input {
        margin-bottom: 1;
    }

    Select {
        margin-bottom: 1;
    }

    .title {
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
    }
    """

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Static("Calculator Inputs", classes="title")

        yield Label("Principal Amount ($)")
        yield Input(value="10000", placeholder="10000", type="number", id="principal_input")

        yield Label("Annual Return Rate (%)")
        yield Input(value="7", placeholder="7", type="number", id="rate_input")

        yield Label("Years")
        yield Input(value="10", placeholder="10", type="integer", id="years_input")

        yield Label("Months")
        yield Input(value="0", placeholder="0", type="integer", id="months_input")

        yield Label("Monthly Contribution ($)")
        yield Input(value="500", placeholder="500", type="number", id="monthly_contrib_input")

        yield Label("Annual Contribution ($)")
        yield Input(value="0", placeholder="0", type="number", id="annual_contrib_input")

        yield Label("Compounding Frequency")
        yield Select(
            options=[
                ("Monthly", CompoundingFrequency.MONTHLY),
                ("Annually", CompoundingFrequency.ANNUALLY),
                ("Daily", CompoundingFrequency.DAILY),
            ],
            value=CompoundingFrequency.MONTHLY,
            id="compounding_select",
        )

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input field changes (blur triggers calculation)."""
        screen = self.screen

        # Map input IDs to screen reactive properties
        if event.input.id == "principal_input":
            try:
                screen.principal = float(event.value) if event.value else 0
            except ValueError:
                pass
        elif event.input.id == "rate_input":
            try:
                screen.annual_rate = float(event.value) if event.value else 0
            except ValueError:
                pass
        elif event.input.id == "years_input":
            try:
                screen.years = int(event.value) if event.value else 0
            except ValueError:
                pass
        elif event.input.id == "months_input":
            try:
                screen.months = int(event.value) if event.value else 0
            except ValueError:
                pass
        elif event.input.id == "monthly_contrib_input":
            try:
                screen.monthly_contribution = float(event.value) if event.value else 0
            except ValueError:
                pass
        elif event.input.id == "annual_contrib_input":
            try:
                screen.annual_contribution = float(event.value) if event.value else 0
            except ValueError:
                pass

    def on_select_changed(self, event: Select.Changed) -> None:
        """Handle select dropdown changes."""
        if event.select.id == "compounding_select":
            self.screen.compounding_frequency = event.value

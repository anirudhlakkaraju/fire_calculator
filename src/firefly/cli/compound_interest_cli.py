"""Interactive CLI for compound interest calculator."""

import questionary
from questionary import Style
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from firefly.cli.visualizer import CompoundInterestVisualizer
from firefly.core.calculators.compound_interest_calculator import (
    CompoundInterestCalculator,
)
from firefly.core.models.compound_interest import (
    CompoundingFrequency,
    CompoundInterestInput,
)

custom_style = Style(
    [
        ("qmark", "fg:#673ab7 bold"),
        ("question", "bold"),
        ("answer", "fg:#f44336 bold"),
        ("pointer", "fg:#673ab7 bold"),
        ("highlighted", "fg:#673ab7 bold"),
        ("selected", "fg:#cc5454"),
        ("separator", "fg:#cc5454"),
        ("instruction", ""),
        ("text", ""),
    ]
)


class CompoundInterestCLI:
    """Interactive CLI for compound interest calculations."""

    def __init__(self):
        self.calculator = CompoundInterestCalculator()
        self.visualizer = CompoundInterestVisualizer()
        self.console = Console()
        # In-memory cache for last used parameters
        self.last_input: CompoundInterestInput | None = None

    def run(self) -> None:
        """Run the interactive CLI."""
        self._show_welcome()

        while True:
            params = self._gather_inputs()
            if params is None:
                break

            # Show summary and confirm
            if not self._confirm_inputs(params):
                continue

            # Cache the parameters
            self.last_input = params

            result = self.calculator.calculate(params)

            # Ask about yearly breakdown
            show_yearly = questionary.confirm(
                "Show year-by-year breakdown?", default=False, style=custom_style
            ).ask()

            self.visualizer.display_all(result, show_yearly=show_yearly)

            # Ask what to do next
            action = questionary.select(
                "What would you like to do?",
                choices=["Adjust parameters", "New calculation", "Exit"],
                style=custom_style,
            ).ask()

            if action == "Exit":
                self.console.print("\n[cyan]Thanks for using Firefly! 🔥[/cyan]")
                break
            elif action == "New calculation":
                continue
            # "Adjust parameters" loops back with cached values

    def _show_welcome(self) -> None:
        """Show welcome message with instructions."""
        welcome_text = """
[bold cyan]🔥 Firefly - Compound Interest Calculator[/bold cyan]

[dim]Keyboard shortcuts:[/dim]
  [yellow]Enter[/yellow] - Confirm selection
  [yellow]↑/↓[/yellow] arrows - Navigate options
  [yellow]Ctrl+C[/yellow] or [yellow]Ctrl+D[/yellow] - Exit anytime

Like a firefly lighting your path to financial independence!
        """
        self.console.print(Panel(welcome_text, border_style="cyan"))

    def _confirm_inputs(self, params: CompoundInterestInput) -> bool:
        """Show summary of inputs and allow editing."""
        while True:
            # Display summary table
            table = Table(title="📋 Input Summary", show_header=False, border_style="cyan")
            table.add_column("Parameter", style="cyan", no_wrap=True)
            table.add_column("Value", style="yellow")

            table.add_row("Principal", f"${params.principal:,.2f}")
            table.add_row("Annual Return Rate", f"{params.annual_rate}%")
            table.add_row("Time Period", f"{params.years} years, {params.months} months")
            table.add_row("Compounding", params.compounding_frequency.name.title())

            if params.monthly_contribution > 0:
                table.add_row("Monthly Contribution", f"${params.monthly_contribution:,.2f}")
            elif params.annual_contribution > 0:
                table.add_row("Annual Contribution", f"${params.annual_contribution:,.2f}")
            else:
                table.add_row("Contributions", "None")

            self.console.print()
            self.console.print(table)
            self.console.print()

            # Ask to confirm or edit
            action = questionary.select(
                "Does this look correct?",
                choices=[
                    "Yes, calculate!",
                    "Edit Principal",
                    "Edit Return Rate",
                    "Edit Time Period",
                    "Edit Compounding Frequency",
                    "Edit Contributions",
                    "Cancel",
                ],
                style=custom_style,
            ).ask()

            if action == "Yes, calculate!":
                return True
            elif action == "Cancel":
                return False
            elif action == "Edit Principal":
                new_val = self._ask_principal(str(params.principal))
                if new_val is not None:
                    params.principal = new_val
            elif action == "Edit Return Rate":
                new_val = self._ask_return_rate(str(params.annual_rate))
                if new_val is not None:
                    params.annual_rate = new_val
            elif action == "Edit Time Period":
                years, months = self._ask_time_period(params.years, params.months)
                if years is not None:
                    params.years = years
                    params.months = months
            elif action == "Edit Compounding Frequency":
                new_val = self._ask_compounding()
                if new_val is not None:
                    params.compounding_frequency = new_val
            elif action == "Edit Contributions":
                monthly, annual = self._ask_contributions(
                    params.monthly_contribution, params.annual_contribution
                )
                params.monthly_contribution = monthly
                params.annual_contribution = annual

    def _gather_inputs(self) -> CompoundInterestInput | None:
        """Gather inputs from user through interactive prompts."""
        try:
            # Use cached values as defaults
            default_principal = str(int(self.last_input.principal)) if self.last_input else ""
            default_rate = str(self.last_input.annual_rate) if self.last_input else "7"
            default_years = self.last_input.years if self.last_input else 10
            default_months = self.last_input.months if self.last_input else 0
            default_monthly_contrib = self.last_input.monthly_contribution if self.last_input else 0
            default_annual_contrib = self.last_input.annual_contribution if self.last_input else 0

            # Principal amount
            principal = self._ask_principal(default_principal)
            if principal is None:
                return None

            # Annual return rate
            annual_rate = self._ask_return_rate(default_rate)
            if annual_rate is None:
                return None

            # Time period
            years, months = self._ask_time_period(default_years, default_months)
            if years is None:
                return None

            # Compounding frequency
            compounding_frequency = self._ask_compounding()
            if compounding_frequency is None:
                return None

            # Contributions
            monthly_contribution, annual_contribution = self._ask_contributions(
                default_monthly_contrib, default_annual_contrib
            )

            return CompoundInterestInput(
                principal=principal,
                annual_rate=annual_rate,
                years=years,
                months=months,
                monthly_contribution=monthly_contribution,
                annual_contribution=annual_contribution,
                compounding_frequency=compounding_frequency,
            )

        except KeyboardInterrupt:
            return None

    def _ask_principal(self, default: str) -> float | None:
        """Ask for principal amount."""
        principal = questionary.text(
            "Principal amount ($):",
            default=default,
            validate=lambda x: x.replace(".", "").replace(",", "").isdigit()
            and float(x.replace(",", "")) > 0,
            style=custom_style,
        ).ask()
        if principal is None:
            return None
        return float(principal.replace(",", ""))

    def _ask_return_rate(self, default: str = "7") -> float | None:
        """Ask for annual return rate."""
        annual_rate = questionary.text(
            "Annual return rate (%):",
            default=default,
            validate=lambda x: x.replace(".", "").isdigit() and float(x) >= 0,
            style=custom_style,
        ).ask()
        if annual_rate is None:
            return None
        return float(annual_rate)

    def _ask_time_period(
        self, default_years: int = 10, default_months: int = 0
    ) -> tuple[int | None, int]:
        """Ask for time period."""
        time_choice = questionary.select(
            "Time period:",
            choices=["Years only", "Years + Months"],
            style=custom_style,
        ).ask()

        years = questionary.text(
            "Years:",
            default=str(default_years),
            validate=lambda x: x.isdigit() and int(x) >= 0,
            style=custom_style,
        ).ask()
        if years is None:
            return None, 0
        years = int(years)

        months = 0
        if time_choice == "Years + Months":
            months_input = questionary.text(
                "Months:",
                default=str(default_months),
                validate=lambda x: x.isdigit() and 0 <= int(x) < 12,
                style=custom_style,
            ).ask()
            if months_input is None:
                return None, 0
            months = int(months_input)

        return years, months

    def _ask_compounding(self) -> CompoundingFrequency | None:
        """Ask for compounding frequency."""
        compounding = questionary.select(
            "Compounding frequency:",
            choices=["Monthly", "Annually", "Daily"],
            style=custom_style,
        ).ask()

        if compounding is None:
            return None

        compounding_map = {
            "Monthly": CompoundingFrequency.MONTHLY,
            "Annually": CompoundingFrequency.ANNUALLY,
            "Daily": CompoundingFrequency.DAILY,
        }
        return compounding_map[compounding]

    def _ask_contributions(
        self, default_monthly: float = 0, default_annual: float = 0
    ) -> tuple[float, float]:
        """Ask for contribution amounts."""
        # Determine default choice
        default_choice = "No contributions"
        if default_monthly > 0:
            default_choice = "Monthly contributions"
        elif default_annual > 0:
            default_choice = "Annual contributions"

        contribution_choice = questionary.select(
            "Do you want to add regular contributions?",
            choices=[
                "No contributions",
                "Monthly contributions",
                "Annual contributions",
            ],
            default=default_choice,
            style=custom_style,
        ).ask()

        monthly_contribution = 0
        annual_contribution = 0

        if contribution_choice == "Monthly contributions":
            monthly_input = questionary.text(
                "Monthly contribution amount ($):",
                default=str(int(default_monthly)) if default_monthly > 0 else "0",
                validate=lambda x: x.replace(".", "").replace(",", "").isdigit()
                and float(x.replace(",", "")) >= 0,
                style=custom_style,
            ).ask()
            if monthly_input is not None:
                monthly_contribution = float(monthly_input.replace(",", ""))

        elif contribution_choice == "Annual contributions":
            annual_input = questionary.text(
                "Annual contribution amount ($):",
                default=str(int(default_annual)) if default_annual > 0 else "0",
                validate=lambda x: x.replace(".", "").replace(",", "").isdigit()
                and float(x.replace(",", "")) >= 0,
                style=custom_style,
            ).ask()
            if annual_input is not None:
                annual_contribution = float(annual_input.replace(",", ""))

        return monthly_contribution, annual_contribution


def main():
    """Entry point for compound interest CLI."""
    cli = CompoundInterestCLI()
    cli.run()


if __name__ == "__main__":
    main()

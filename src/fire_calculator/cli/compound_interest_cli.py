"""Interactive CLI for compound interest calculator."""

import questionary
from questionary import Style

from fire_calculator.calculators.compound_interest_calculator import (
    CompoundInterestCalculator,
)
from fire_calculator.cli.visualizer import CompoundInterestVisualizer
from fire_calculator.models.compound_interest import (
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

    def run(self) -> None:
        """Run the interactive CLI."""
        while True:
            params = self._gather_inputs()
            if params is None:
                break

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
                break
            elif action == "New calculation":
                continue

    def _gather_inputs(self) -> CompoundInterestInput | None:
        """Gather inputs from user through interactive prompts."""
        try:
            # Principal amount
            principal = questionary.text(
                "Principal amount ($):",
                validate=lambda x: x.replace(".", "").replace(",", "").isdigit()
                and float(x.replace(",", "")) > 0,
                style=custom_style,
            ).ask()
            if principal is None:
                return None
            principal = float(principal.replace(",", ""))

            # Annual return rate
            annual_rate = questionary.text(
                "Annual return rate (%):",
                default="7",
                validate=lambda x: x.replace(".", "").isdigit() and float(x) >= 0,
                style=custom_style,
            ).ask()
            if annual_rate is None:
                return None
            annual_rate = float(annual_rate)

            # Time period
            time_choice = questionary.select(
                "Time period:",
                choices=["Years only", "Years + Months"],
                style=custom_style,
            ).ask()

            years = questionary.text(
                "Years:",
                default="10",
                validate=lambda x: x.isdigit() and int(x) >= 0,
                style=custom_style,
            ).ask()
            if years is None:
                return None
            years = int(years)

            months = 0
            if time_choice == "Years + Months":
                months = questionary.text(
                    "Months:",
                    default="0",
                    validate=lambda x: x.isdigit() and 0 <= int(x) < 12,
                    style=custom_style,
                ).ask()
                if months is None:
                    return None
                months = int(months)

            # Compounding frequency
            compounding = questionary.select(
                "Compounding frequency:",
                choices=["Monthly", "Annually", "Daily"],
                style=custom_style,
            ).ask()

            compounding_map = {
                "Monthly": CompoundingFrequency.MONTHLY,
                "Annually": CompoundingFrequency.ANNUALLY,
                "Daily": CompoundingFrequency.DAILY,
            }
            compounding_frequency = compounding_map[compounding]

            # Contributions
            contribution_choice = questionary.select(
                "Do you want to add regular contributions?",
                choices=[
                    "No contributions",
                    "Monthly contributions",
                    "Annual contributions",
                ],
                style=custom_style,
            ).ask()

            monthly_contribution = 0
            annual_contribution = 0

            if contribution_choice == "Monthly contributions":
                monthly_contribution = questionary.text(
                    "Monthly contribution amount ($):",
                    default="0",
                    validate=lambda x: x.replace(".", "").replace(",", "").isdigit()
                    and float(x.replace(",", "")) >= 0,
                    style=custom_style,
                ).ask()
                if monthly_contribution is None:
                    return None
                monthly_contribution = float(monthly_contribution.replace(",", ""))

            elif contribution_choice == "Annual contributions":
                annual_contribution = questionary.text(
                    "Annual contribution amount ($):",
                    default="0",
                    validate=lambda x: x.replace(".", "").replace(",", "").isdigit()
                    and float(x.replace(",", "")) >= 0,
                    style=custom_style,
                ).ask()
                if annual_contribution is None:
                    return None
                annual_contribution = float(annual_contribution.replace(",", ""))

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


def main():
    """Entry point for compound interest CLI."""
    cli = CompoundInterestCLI()
    cli.run()


if __name__ == "__main__":
    main()

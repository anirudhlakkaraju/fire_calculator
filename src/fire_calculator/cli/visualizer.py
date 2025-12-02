"""Visualization tools for compound interest results."""

import plotext as plt
from rich.console import Console
from rich.table import Table

from fire_calculator.models.compound_interest import CompoundInterestResult


class CompoundInterestVisualizer:
    """Visualizer for compound interest calculations."""

    def __init__(self):
        self.console = Console()

    def display_summary(self, result: CompoundInterestResult) -> None:
        """Display summary of results."""
        params = result.input_params

        # Create summary table
        table = Table(title="📊 Compound Interest Summary", show_header=False)
        table.add_column("Parameter", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")

        # Input parameters
        table.add_row("Initial Investment", f"${params.principal:,.2f}")
        table.add_row("Annual Return Rate", f"{params.annual_rate}%")
        table.add_row("Time Period", f"{params.years} years, {params.months} months")
        table.add_row("Compounding", params.compounding_frequency.name.title())

        if params.monthly_contribution > 0:
            table.add_row(
                "Monthly Contribution", f"${params.monthly_contribution:,.2f}"
            )
        if params.annual_contribution > 0:
            table.add_row("Annual Contribution", f"${params.annual_contribution:,.2f}")

        table.add_section()

        # Results
        table.add_row(
            "Final Amount", f"${result.final_amount:,.2f}", style="bold green"
        )
        table.add_row("Total Contributions", f"${result.total_contributions:,.2f}")
        table.add_row(
            "Total Interest Earned",
            f"${result.total_interest:,.2f}",
            style="bold yellow",
        )

        self.console.print(table)

    def display_yearly_breakdown(self, result: CompoundInterestResult) -> None:
        """Display year-by-year breakdown."""
        table = Table(title="📅 Year-by-Year Breakdown")

        table.add_column("Year", justify="right", style="cyan")
        table.add_column("Starting Balance", justify="right", style="white")
        table.add_column("Contributions", justify="right", style="blue")
        table.add_column("Interest Earned", justify="right", style="yellow")
        table.add_column("Ending Balance", justify="right", style="green")

        for year_data in result.yearly_breakdown:
            table.add_row(
                str(year_data.year),
                f"${year_data.starting_balance:,.2f}",
                f"${year_data.contributions:,.2f}",
                f"${year_data.interest_earned:,.2f}",
                f"${year_data.ending_balance:,.2f}",
            )

        self.console.print(table)

    def display_graph(self, result: CompoundInterestResult) -> None:
        """Display ASCII graph of portfolio growth."""
        params = result.input_params

        # Generate monthly data points for smoother graphs
        monthly_data = self._generate_monthly_data(result)

        months = monthly_data["months"]
        balances = monthly_data["balances"]
        contributions_cumulative = monthly_data["contributions"]

        plt.clear_figure()
        plt.plot_size(100, 30)

        # Plot ending balance
        plt.plot(months, balances, label="Total Balance", marker="braille")

        # Plot cumulative contributions
        plt.plot(
            months,
            contributions_cumulative,
            label="Principal + Contributions",
            marker="braille",
        )

        plt.title("Portfolio Growth Over Time")
        plt.xlabel("Month" if params.total_periods <= 3 else "Year")
        plt.ylabel("Amount ($)")
        plt.theme("clear")

        plt.show()

    def _generate_monthly_data(self, result: CompoundInterestResult) -> dict:
        """Generate monthly data points for smoother visualization."""
        params = result.input_params

        months = []
        balances = []
        contributions = []

        balance = params.principal
        cumulative_contrib = params.principal

        n = params.compounding_frequency.value
        r = params.rate_decimal

        # Determine contribution per month
        monthly_contribution = (
            params.monthly_contribution
            if params.monthly_contribution > 0
            else params.annual_contribution / 12
        )

        # Calculate total months
        total_months = int(params.total_periods * 12)

        # Add initial point
        months.append(0)
        balances.append(balance)
        contributions.append(cumulative_contrib)

        # Calculate monthly snapshots
        for month in range(1, total_months + 1):
            # Calculate interest for this month based on compounding frequency
            if n == 12:  # Monthly compounding
                month_interest = balance * (r / 12)
                balance += month_interest
                balance += monthly_contribution
                cumulative_contrib += monthly_contribution
            elif n == 365:  # Daily compounding
                # Compound daily for ~30 days
                for day in range(30):
                    balance += balance * (r / 365)
                    balance += monthly_contribution / 30
                    cumulative_contrib += monthly_contribution / 30
            else:  # Annual compounding
                # Apply monthly contribution, but compound interest yearly
                if month % 12 == 0:
                    balance += balance * r
                balance += monthly_contribution
                cumulative_contrib += monthly_contribution

            # Convert to years for display if period > 3 years
            time_value = month / 12 if params.total_periods > 3 else month

            months.append(time_value)
            balances.append(balance)
            contributions.append(cumulative_contrib)

        return {"months": months, "balances": balances, "contributions": contributions}

    def display_all(
        self, result: CompoundInterestResult, show_yearly: bool = False
    ) -> None:
        """Display all visualizations."""
        self.console.print()
        self.display_summary(result)
        self.console.print()

        if show_yearly:
            self.display_yearly_breakdown(result)
            self.console.print()

        self.display_graph(result)
        self.console.print()

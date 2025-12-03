"""Graphing utilities for TUI."""

import io
from contextlib import redirect_stdout

import plotext as plt

from firefly.core.models.compound_interest import CompoundInterestResult


def generate_ascii_graph(result: CompoundInterestResult) -> str:
    """Generate ASCII graph from calculation result."""
    params = result.input_params

    # Extract data
    years = [yb.year for yb in result.yearly_breakdown]
    balances = [yb.ending_balance for yb in result.yearly_breakdown]

    # Calculate cumulative contributions
    cumulative_contrib = params.principal
    contributions_line = [cumulative_contrib]
    for yb in result.yearly_breakdown[:-1]:
        cumulative_contrib += yb.contributions
        contributions_line.append(cumulative_contrib)

    # Clear and configure plot
    plt.clear_figure()
    plt.plot_size(60, 20)

    # Plot lines
    plt.plot(years, balances, label="Total Balance", marker="braille")
    plt.plot(years, contributions_line, label="Principal + Contributions", marker="braille")

    # Styling
    plt.title("Portfolio Growth Over Time")
    plt.xlabel("Year")
    plt.ylabel("Amount ($)")
    plt.theme("clear")

    # Capture output
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        plt.show()

    return buffer.getvalue()

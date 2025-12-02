"""Firefly - Financial Independence Calculator.

A CLI tool for compound interest calculations and FIRE planning.
"""

__version__ = "0.1.0"

# Public API exports (for programmatic use)
from firefly.core.calculators.compound_interest_calculator import (
    CompoundInterestCalculator,
)
from firefly.core.models.compound_interest import (
    CompoundingFrequency,
    CompoundInterestInput,
    CompoundInterestResult,
    YearlyBreakdown,
)

__all__ = [
    "CompoundInterestCalculator",
    "CompoundInterestInput",
    "CompoundInterestResult",
    "YearlyBreakdown",
    "CompoundingFrequency",
]

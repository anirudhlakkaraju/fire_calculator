"""Data models for compound interest calculations."""

from dataclasses import dataclass
from enum import Enum


class CompoundingFrequency(Enum):
    """Frequency of compounding."""

    DAILY = 365
    MONTHLY = 12
    ANNUALLY = 1


class ContributionFrequency(Enum):
    """Frequency of contributions."""

    MONTHLY = 12
    ANNUALLY = 1


@dataclass
class CompoundInterestInput:
    """Input parameters for compound interest calculation."""

    principal: float
    annual_rate: float  # as percentage, e.g., 7 for 7%
    years: int
    months: int = 0
    monthly_contribution: float = 0
    annual_contribution: float = 0
    compounding_frequency: CompoundingFrequency = CompoundingFrequency.MONTHLY

    @property
    def total_periods(self) -> float:
        """Total time period in years."""
        return self.years + (self.months / 12)

    @property
    def rate_decimal(self) -> float:
        """Annual rate as decimal."""
        return self.annual_rate / 100


@dataclass
class YearlyBreakdown:
    """Breakdown for a specific year."""

    year: int
    starting_balance: float
    contributions: float
    interest_earned: float
    ending_balance: float


@dataclass
class CompoundInterestResult:
    """Result of compound interest calculation."""

    final_amount: float
    total_contributions: float
    total_interest: float
    yearly_breakdown: list[YearlyBreakdown]
    input_params: CompoundInterestInput

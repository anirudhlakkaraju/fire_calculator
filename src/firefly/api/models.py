"""API request and response models."""

from pydantic import BaseModel, Field


class CalculateRequest(BaseModel):
    """Request model for compound interest calculation."""

    principal: float = Field(description="Initial investment amount in dollars", gt=0)
    annual_rate: float = Field(description="Annual return rate as a percentage (e.g., 7 for 7%)")
    years: int = Field(description="Number of years to calculate", gt=0)
    months: int = Field(0, description="Additional months beyond years", ge=0)
    monthly_contribution: float = Field(
        0, description="Amount contributed each month in dollars", ge=0
    )
    annual_contribution: float = Field(
        0, description="Amount contributed each year in dollars", ge=0
    )
    compounding_frequency: str = Field(
        "annually", description="How often interest compounds: 'daily', 'monthly', or 'annually'"
    )


class YearlyBreakdownItem(BaseModel):
    """Single year's breakdown data."""

    year: int
    starting_balance: float
    contributions: float
    interest_earned: float
    ending_balance: float


class CalculateResponse(BaseModel):
    """Response model with calculation results."""

    final_amount: float = Field(description="Total portfolio value at the end")
    total_contributions: float = Field(description="Sum of all contributions made")
    total_interest: float = Field(description="Total interest earned over the period")
    yearly_breakdown: list[YearlyBreakdownItem] = Field(
        description="Year-by-year breakdown for graphing"
    )

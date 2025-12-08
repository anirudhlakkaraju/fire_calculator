"""Calculator API Routes"""

from fastapi import APIRouter, HTTPException

from firefly.api.models import CalculateRequest, CalculateResponse, YearlyBreakdownItem
from firefly.core.calculators.compound_interest import CompoundInterestCalculator
from firefly.core.models.compound_interest import CompoundingFrequency, CompoundInterestInput

router = APIRouter()

# Map string values to CompoundingFrequency enum
FREQUENCY_MAP = {
    "daily": CompoundingFrequency.DAILY,
    "monthly": CompoundingFrequency.MONTHLY,
    "annually": CompoundingFrequency.ANNUALLY,
}


@router.post("/api/calculate", response_model=CalculateResponse)
def calculate(request: CalculateRequest) -> CalculateResponse:
    """Calculate compound interest based on input parameters."""

    # Convert string to enum
    compounding_freq = FREQUENCY_MAP.get(request.compounding_frequency.lower())
    if not compounding_freq:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid compounding_frequency: {request.compounding_frequency}. Must be 'daily', 'monthly', or 'annually'.",
        )

    # Create core model from API request
    params = CompoundInterestInput(
        principal=request.principal,
        annual_rate=request.annual_rate,
        years=request.years,
        months=request.months,
        monthly_contribution=request.monthly_contribution,
        annual_contribution=request.annual_contribution,
        compounding_frequency=compounding_freq,
    )

    # Calculate using core logic
    calculator = CompoundInterestCalculator()
    result = calculator.calculate(params)

    # Convert core result to API response
    yearly_breakdown = [
        YearlyBreakdownItem(
            year=yb.year,
            starting_balance=yb.starting_balance,
            contributions=yb.contributions,
            interest_earned=yb.interest_earned,
            ending_balance=yb.ending_balance,
        )
        for yb in result.yearly_breakdown
    ]

    return CalculateResponse(
        final_amount=result.final_amount,
        total_contributions=result.total_contributions,
        total_interest=result.total_interest,
        yearly_breakdown=yearly_breakdown,
    )

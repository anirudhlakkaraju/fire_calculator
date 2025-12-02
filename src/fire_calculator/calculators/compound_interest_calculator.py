"""Compound interest calculator implementation."""


from fire_calculator.models.compound_interest import (
    CompoundInterestInput,
    CompoundInterestResult,
    YearlyBreakdown,
)


class CompoundInterestCalculator:
    """Calculator for compound interest with regular contributions."""

    def calculate(self, params: CompoundInterestInput) -> CompoundInterestResult:
        """
        Calculate compound interest with contributions.

        Formula:
        FV = P(1 + r/n)^(nt) + PMT × [((1 + r/n)^(nt) - 1) / (r/n)]

        Where:
        - P = principal
        - r = annual interest rate (decimal)
        - n = compounding frequency per year
        - t = time in years
        - PMT = periodic contribution
        """
        yearly_breakdown = self._calculate_yearly_breakdown(params)

        final_amount = yearly_breakdown[-1].ending_balance if yearly_breakdown else params.principal
        total_contributions = sum(yb.contributions for yb in yearly_breakdown)
        total_interest = final_amount - params.principal - total_contributions

        return CompoundInterestResult(
            final_amount=final_amount,
            total_contributions=total_contributions,
            total_interest=total_interest,
            yearly_breakdown=yearly_breakdown,
            input_params=params,
        )

    def _calculate_yearly_breakdown(self, params: CompoundInterestInput) -> list[YearlyBreakdown]:
        """Calculate year-by-year breakdown."""
        breakdown = []
        balance = params.principal

        # Calculate total periods (considering months)
        total_years = params.total_periods

        # Determine contribution per compounding period
        n = params.compounding_frequency.value
        r = params.rate_decimal

        # Convert contributions to per-period amounts
        if params.monthly_contribution > 0:
            # Monthly contributions
            if params.compounding_frequency.value == 12:  # Monthly compounding
                contribution_per_period = params.monthly_contribution
            elif params.compounding_frequency.value == 365:  # Daily compounding
                contribution_per_period = params.monthly_contribution / 30.417  # avg days per month
            else:  # Annual compounding
                contribution_per_period = params.monthly_contribution * 12
        else:
            # Annual contributions
            if params.compounding_frequency.value == 12:  # Monthly compounding
                contribution_per_period = params.annual_contribution / 12
            elif params.compounding_frequency.value == 365:  # Daily compounding
                contribution_per_period = params.annual_contribution / 365
            else:  # Annual compounding
                contribution_per_period = params.annual_contribution

        # Calculate for each year
        for year in range(1, int(total_years) + 2):
            starting_balance = balance
            year_contributions = 0
            year_interest = 0

            # Determine how many periods to calculate for this year
            if year <= total_years:
                periods_this_year = n if year < total_years else int((total_years - (year - 1)) * n)
            else:
                break

            # Calculate each period within the year
            for _ in range(periods_this_year):
                # Add interest
                period_interest = balance * (r / n)
                balance += period_interest
                year_interest += period_interest

                # Add contribution
                balance += contribution_per_period
                year_contributions += contribution_per_period

            ending_balance = balance

            breakdown.append(
                YearlyBreakdown(
                    year=year,
                    starting_balance=starting_balance,
                    contributions=year_contributions,
                    interest_earned=year_interest,
                    ending_balance=ending_balance,
                )
            )

        return breakdown

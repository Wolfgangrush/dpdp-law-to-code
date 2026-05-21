"""Example — check whether processing of employee data fits DPDP Sec 7(g).

Run:
    python examples/employee_data_legitimacy.py
"""

from __future__ import annotations

from dpdp.legitimate import check_legitimate_use
from dpdp.types import LegitimateUseCase, LegitimateUseRecord


def main() -> None:
    # Scenario A — HR processing salary + performance data of current employee.
    payroll = LegitimateUseRecord(
        asserted_case=LegitimateUseCase.EMPLOYMENT_PURPOSES,
        purpose_description="payroll processing and performance review",
        is_employment_related=True,
    )
    print("Scenario A — payroll under Sec 7(g):")
    print(check_legitimate_use(payroll))
    print()

    # Scenario B — startup tries to claim 7(g) for processing personal data
    # of prospects scraped from LinkedIn. NOT an employment relationship.
    sales_prospects = LegitimateUseRecord(
        asserted_case=LegitimateUseCase.EMPLOYMENT_PURPOSES,
        purpose_description="enrich CRM with LinkedIn-scraped prospect data",
        is_employment_related=False,
    )
    print("Scenario B — sales prospects mis-claimed as Sec 7(g):")
    print(check_legitimate_use(sales_prospects))
    print()

    # Scenario C — hospital invokes Sec 7(d) medical emergency for unconscious
    # patient.
    er = LegitimateUseRecord(
        asserted_case=LegitimateUseCase.MEDICAL_EMERGENCY,
        purpose_description="ER admission of unconscious road-accident patient",
        threatens_life_or_health=True,
    )
    print("Scenario C — Sec 7(d) medical emergency:")
    print(check_legitimate_use(er))


if __name__ == "__main__":
    main()

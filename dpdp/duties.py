"""Sec 15 — Duties of Data Principal.

Citation: DPDP Act 2023, Sec 15.
Last updated: 2026-05-23.

Sec 15(a) — comply with applicable laws while exercising rights.
Sec 15(b) — no impersonation while providing personal data.
Sec 15(c) — no suppression of material information for State documents.
Sec 15(d) — no false or frivolous grievance/complaint.
Sec 15(e) — furnish only verifiably authentic information for correction/erasure.

Breach of any Sec 15 duty attracts penalty up to ₹10,000 per Schedule Row 5.

This module is not legal advice. It encodes a developer-friendly reading of
DPDP Act 2023 Sec 15 for compliance harness purposes. Consult qualified
counsel before relying on outputs for regulatory or contentious matters.
"""

from __future__ import annotations

from dpdp.exceptions import InvalidInputError
from dpdp.types import ComplianceResult, DataPrincipalDuty

_DUTY_PENALTY_CAP_INR = 10_000


def check_sec_15_a(complies_with_applicable_laws: bool) -> ComplianceResult:
    """Sec 15(a) — Data Principal shall comply with all applicable laws while exercising rights."""
    if not isinstance(complies_with_applicable_laws, bool):
        raise InvalidInputError(
            "complies_with_applicable_laws must be bool", section="Sec 15(a)"
        )

    if complies_with_applicable_laws:
        return ComplianceResult(
            compliant=True,
            section="Sec 15(a)",
            reason="complies with applicable laws while exercising rights",
            citation="DPDP Act 2023, Sec 15(a)",
        )
    return ComplianceResult(
        compliant=False,
        section="Sec 15(a)",
        reason=f"failed to comply with applicable laws while exercising rights — penalty up to ₹{_DUTY_PENALTY_CAP_INR:,}",
        citation="DPDP Act 2023, Sec 15(a)",
    )


def check_sec_15_b(duty: DataPrincipalDuty) -> ComplianceResult:
    """Sec 15(b) — Data Principal shall not impersonate another person."""
    if not isinstance(duty, DataPrincipalDuty):
        raise InvalidInputError("expected DataPrincipalDuty", section="Sec 15(b)")

    if not duty.impersonated_another_person:
        return ComplianceResult(
            compliant=True,
            section="Sec 15(b)",
            reason="no impersonation — Sec 15(b) satisfied",
            citation="DPDP Act 2023, Sec 15(b)",
        )
    return ComplianceResult(
        compliant=False,
        section="Sec 15(b)",
        reason=f"impersonated another person — Sec 15(b) breach, penalty up to ₹{_DUTY_PENALTY_CAP_INR:,}",
        citation="DPDP Act 2023, Sec 15(b)",
    )


def check_sec_15_c(duty: DataPrincipalDuty) -> ComplianceResult:
    """Sec 15(c) — Data Principal shall not suppress material information for State-issued documents."""
    if not isinstance(duty, DataPrincipalDuty):
        raise InvalidInputError("expected DataPrincipalDuty", section="Sec 15(c)")

    breaches: list[ComplianceResult] = []

    if duty.submitted_false_particulars:
        breaches.append(
            ComplianceResult(
                compliant=False,
                section="Sec 15(c)",
                reason=f"submitted false particulars — Sec 15(c) breach, penalty up to ₹{_DUTY_PENALTY_CAP_INR:,}",
                citation="DPDP Act 2023, Sec 15(c)",
            )
        )
    if duty.suppressed_material_information:
        breaches.append(
            ComplianceResult(
                compliant=False,
                section="Sec 15(c)",
                reason=f"suppressed material information — Sec 15(c) breach, penalty up to ₹{_DUTY_PENALTY_CAP_INR:,}",
                citation="DPDP Act 2023, Sec 15(c)",
            )
        )

    if not breaches:
        return ComplianceResult(
            compliant=True,
            section="Sec 15(c)",
            reason="no suppression or false particulars — Sec 15(c) satisfied",
            citation="DPDP Act 2023, Sec 15(c)",
        )

    return ComplianceResult(
        compliant=False,
        section="Sec 15(c)",
        reason="; ".join(b.reason for b in breaches),
        citation="DPDP Act 2023, Sec 15(c)",
        sub_results=breaches,
    )


def check_sec_15_d(duty: DataPrincipalDuty) -> ComplianceResult:
    """Sec 15(d) — Data Principal shall not register a false or frivolous grievance/complaint."""
    if not isinstance(duty, DataPrincipalDuty):
        raise InvalidInputError("expected DataPrincipalDuty", section="Sec 15(d)")

    breaches: list[ComplianceResult] = []

    if duty.filed_frivolous_grievance:
        breaches.append(
            ComplianceResult(
                compliant=False,
                section="Sec 15(d)",
                reason=f"frivolous grievance — Sec 15(d) breach, penalty up to ₹{_DUTY_PENALTY_CAP_INR:,}",
                citation="DPDP Act 2023, Sec 15(d)",
            )
        )
    if duty.filed_false_complaint:
        breaches.append(
            ComplianceResult(
                compliant=False,
                section="Sec 15(d)",
                reason=f"false complaint — Sec 15(d) breach, penalty up to ₹{_DUTY_PENALTY_CAP_INR:,}",
                citation="DPDP Act 2023, Sec 15(d)",
            )
        )

    if not breaches:
        return ComplianceResult(
            compliant=True,
            section="Sec 15(d)",
            reason="no false or frivolous grievance/complaint — Sec 15(d) satisfied",
            citation="DPDP Act 2023, Sec 15(d)",
        )

    return ComplianceResult(
        compliant=False,
        section="Sec 15(d)",
        reason="; ".join(b.reason for b in breaches),
        citation="DPDP Act 2023, Sec 15(d)",
        sub_results=breaches,
    )


def check_sec_15_e(
    furnishes_verifiably_authentic_information: bool,
) -> ComplianceResult:
    """Sec 15(e) — Data Principal shall furnish only verifiably authentic information for correction/erasure."""
    if not isinstance(furnishes_verifiably_authentic_information, bool):
        raise InvalidInputError(
            "furnishes_verifiably_authentic_information must be bool",
            section="Sec 15(e)",
        )

    if furnishes_verifiably_authentic_information:
        return ComplianceResult(
            compliant=True,
            section="Sec 15(e)",
            reason="furnishes verifiably authentic information for correction/erasure",
            citation="DPDP Act 2023, Sec 15(e)",
        )
    return ComplianceResult(
        compliant=False,
        section="Sec 15(e)",
        reason=f"failed to furnish verifiably authentic information — Sec 15(e) breach, penalty up to ₹{_DUTY_PENALTY_CAP_INR:,}",
        citation="DPDP Act 2023, Sec 15(e)",
    )


def check_data_principal_duty(
    duty: DataPrincipalDuty,
    *,
    complies_with_applicable_laws: bool = True,
    furnishes_verifiably_authentic_information: bool = True,
) -> ComplianceResult:
    """Sec 15 — master duty check aggregating sub-clauses (a)-(e)."""
    if not isinstance(duty, DataPrincipalDuty):
        raise InvalidInputError("expected DataPrincipalDuty", section="Sec 15")

    sub: list[ComplianceResult] = []

    sub.append(check_sec_15_a(complies_with_applicable_laws))
    sub.append(check_sec_15_b(duty))
    sub.append(check_sec_15_c(duty))
    sub.append(check_sec_15_d(duty))
    sub.append(check_sec_15_e(furnishes_verifiably_authentic_information))

    breaches = [r for r in sub if not r.compliant]

    if not breaches:
        return ComplianceResult(
            compliant=True,
            section="Sec 15",
            reason="no Sec 15 duty breach detected",
            citation="DPDP Act 2023, Sec 15",
        )

    return ComplianceResult(
        compliant=False,
        section="Sec 15",
        reason=(
            f"{len(breaches)} duty breach(es) — Schedule penalty up to ₹{_DUTY_PENALTY_CAP_INR:,}: "
            + "; ".join(b.reason for b in breaches)
        ),
        citation="DPDP Act 2023, Sec 15",
        sub_results=sub,
    )

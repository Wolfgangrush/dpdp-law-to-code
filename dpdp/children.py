"""Sec 9 — Processing of personal data of children.

Citation: DPDP Act 2023, Sec 9.
Last updated: 2026-05-23.

Sec 9(1) — verifiable parental consent before processing child's personal data.
Sec 9(2) — no processing likely to cause detrimental effect on child's well-being.
Sec 9(3) — no behavioural tracking + no targeted advertising directed at children.
Sec 9(4)/9(5) — Central Government exemption mechanisms.

"Child" = individual who has not completed 18 years of age (per Sec 2).

This module is not legal advice. It encodes a developer-friendly reading of
DPDP Act 2023 Sec 9 for compliance harness purposes. Consult qualified
counsel before relying on outputs for regulatory or contentious matters.
"""

# ═══════════════════════════════════════════════════════════════════════════
# PROPOSED ChildRecord FIELDS (do NOT modify types.py — parallel Sec 10 work)
# ═══════════════════════════════════════════════════════════════════════════
#
# For Sec 9(1) proviso (disability + lawful guardian):
#   is_person_with_disability: bool = False
#   has_lawful_guardian: bool = False
#
# For Sec 9(5) (Central Govt notification lowering age threshold):
#   age_lowered_by_notification: bool = False
#
# These fields are accepted as keyword arguments by check_disability_proviso()
# and check_age_threshold_exemption() respectively until merged into ChildRecord.

from __future__ import annotations

from dpdp.exceptions import InvalidInputError
from dpdp.types import ChildRecord, ComplianceResult


# ═══════════════════════════════════════════════════════════════════════════
# Sec 9(1) — verifiable parental consent
# ═══════════════════════════════════════════════════════════════════════════

def check_parental_consent(record: ChildRecord) -> ComplianceResult:
    """Sec 9(1) — verifiable parental consent before processing child's personal data."""
    # delegated to DPDP Rules 2025 — manner prescribed
    if not isinstance(record, ChildRecord):
        raise InvalidInputError("expected ChildRecord", section="Sec 9(1)")

    return ComplianceResult(
        compliant=record.has_verifiable_parental_consent,
        section="Sec 9(1)",
        reason=("verifiable parental consent obtained" if record.has_verifiable_parental_consent
                else "Sec 9(1) requires verifiable parental consent before processing a child's personal data"),
        citation="DPDP Act 2023, Sec 9(1)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 9(1) proviso — disability + lawful guardian
# ═══════════════════════════════════════════════════════════════════════════

def check_disability_proviso(
    record: ChildRecord,
    is_person_with_disability: bool = False,
    has_lawful_guardian: bool = False,
) -> ComplianceResult:
    """Sec 9(1) proviso — verifiable consent of lawful guardian for persons with disability."""
    if not isinstance(record, ChildRecord):
        raise InvalidInputError("expected ChildRecord", section="Sec 9(1)")

    # proviso only triggers if the Data Principal is a person with disability who has a lawful guardian
    if not is_person_with_disability or not has_lawful_guardian:
        return ComplianceResult(
            compliant=True,
            section="Sec 9(1) proviso",
            reason="Data Principal is not a person with disability with a lawful guardian — proviso not triggered",
            citation="DPDP Act 2023, Sec 9(1) proviso",
        )

    # same verifiable-consent standard applies to lawful guardian as to parent
    return ComplianceResult(
        compliant=record.has_verifiable_parental_consent,
        section="Sec 9(1) proviso",
        reason=("verifiable lawful guardian consent obtained" if record.has_verifiable_parental_consent
                else "Sec 9(1) proviso requires verifiable consent of lawful guardian for persons with disability"),
        citation="DPDP Act 2023, Sec 9(1) proviso",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 9(2) — no detrimental effect on child's well-being
# ═══════════════════════════════════════════════════════════════════════════

def check_detrimental_effect(record: ChildRecord) -> ComplianceResult:
    """Sec 9(2) — no processing likely to cause detrimental effect on child's well-being."""
    if not isinstance(record, ChildRecord):
        raise InvalidInputError("expected ChildRecord", section="Sec 9(2)")

    return ComplianceResult(
        compliant=not record.is_likely_to_cause_detrimental_effect,
        section="Sec 9(2)",
        reason=("processing not detrimental to child's well-being" if not record.is_likely_to_cause_detrimental_effect
                else "Sec 9(2) prohibits processing likely to cause any detrimental effect on a child's well-being"),
        citation="DPDP Act 2023, Sec 9(2)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 9(3) — no behavioural tracking of children
# ═══════════════════════════════════════════════════════════════════════════

def check_tracking_prohibition(record: ChildRecord) -> ComplianceResult:
    """Sec 9(3) — no tracking or behavioural monitoring of children."""
    if not isinstance(record, ChildRecord):
        raise InvalidInputError("expected ChildRecord", section="Sec 9(3)")

    return ComplianceResult(
        compliant=not record.is_tracking_behavior,
        section="Sec 9(3)",
        reason=("no tracking or behavioural monitoring" if not record.is_tracking_behavior
                else "Sec 9(3) prohibits tracking or behavioural monitoring of children"),
        citation="DPDP Act 2023, Sec 9(3)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 9(3) — no targeted advertising directed at children
# ═══════════════════════════════════════════════════════════════════════════

def check_targeted_ads_prohibition(record: ChildRecord) -> ComplianceResult:
    """Sec 9(3) — no targeted advertising directed at children."""
    if not isinstance(record, ChildRecord):
        raise InvalidInputError("expected ChildRecord", section="Sec 9(3)")

    return ComplianceResult(
        compliant=not record.is_targeted_advertising,
        section="Sec 9(3)",
        reason=("no targeted advertising directed at children" if not record.is_targeted_advertising
                else "Sec 9(3) prohibits targeted advertising directed at children"),
        citation="DPDP Act 2023, Sec 9(3)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 9(4) — Central Govt class/purpose exemption
# ═══════════════════════════════════════════════════════════════════════════

def check_class_exemption(record: ChildRecord) -> ComplianceResult:
    """Sec 9(4) — Central Govt may exempt classes of Data Fiduciaries or purposes from 9(1) and 9(3)."""
    if not isinstance(record, ChildRecord):
        raise InvalidInputError("expected ChildRecord", section="Sec 9(4)")

    if record.is_class_exempted_by_notification:
        return ComplianceResult(
            compliant=True,
            section="Sec 9(4)",
            reason="processing falls within Central Govt exemption notification — Sec 9(1) and 9(3) do not apply",
            citation="DPDP Act 2023, Sec 9(4)",
        )

    return ComplianceResult(
        compliant=True,
        section="Sec 9(4)",
        reason="no class exemption notification applies — Sec 9(1) and 9(3) prohibitions apply in full",
        citation="DPDP Act 2023, Sec 9(4)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 9(5) — Central Govt may notify lowered age threshold
# ═══════════════════════════════════════════════════════════════════════════

def check_age_threshold_exemption(
    record: ChildRecord,
    age_lowered_by_notification: bool = False,
) -> ComplianceResult:
    """Sec 9(5) — Central Govt may lower age threshold for Data Fiduciaries processing children's data safely."""
    if not isinstance(record, ChildRecord):
        raise InvalidInputError("expected ChildRecord", section="Sec 9(5)")

    if not age_lowered_by_notification:
        return ComplianceResult(
            compliant=True,
            section="Sec 9(5)",
            reason="no lowered-age notification applies — default 18-year threshold stands",
            citation="DPDP Act 2023, Sec 9(5)",
        )

    # v0.1: bool flag serves as heuristic for "Govt satisfied fiduciary processes
    # children's data safely" — exact lowered-age limit delegated to notification.
    return ComplianceResult(
        compliant=True,
        section="Sec 9(5)",
        reason="Data Fiduciary benefits from Central Govt lowered-age notification — Sec 9(1) and 9(3) exempted for children above notified age",
        citation="DPDP Act 2023, Sec 9(5)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 9 — master compliance check
# ═══════════════════════════════════════════════════════════════════════════

def check_child_processing(
    record: ChildRecord,
    is_person_with_disability: bool = False,
    has_lawful_guardian: bool = False,
    age_lowered_by_notification: bool = False,
) -> ComplianceResult:
    """Sec 9 — master check for processing of children's personal data."""
    if not isinstance(record, ChildRecord):
        raise InvalidInputError("expected ChildRecord", section="Sec 9")

    is_child = record.data_principal_age < 18
    if not is_child:
        return ComplianceResult(
            compliant=True,
            section="Sec 9",
            reason="Data Principal is not a child (>= 18); Sec 9 does not apply",
            citation="DPDP Act 2023, Sec 9",
        )

    if record.is_class_exempted_by_notification:
        return ComplianceResult(
            compliant=True,
            section="Sec 9(4)",
            reason="processing falls within Central Govt exemption notification under Sec 9(4)",
            citation="DPDP Act 2023, Sec 9(4)",
        )

    sub: list[ComplianceResult] = []

    sub.append(check_parental_consent(record))

    sub.append(check_disability_proviso(
        record,
        is_person_with_disability=is_person_with_disability,
        has_lawful_guardian=has_lawful_guardian,
    ))

    sub.append(check_detrimental_effect(record))

    # Sec 9(5) lowered-age exemption overrides 9(3) if applicable
    if not age_lowered_by_notification:
        sub.append(check_tracking_prohibition(record))
        sub.append(check_targeted_ads_prohibition(record))
    else:
        sub.append(check_age_threshold_exemption(
            record,
            age_lowered_by_notification=True,
        ))

    all_pass = all(r.compliant for r in sub)
    failed = [r for r in sub if not r.compliant]
    return ComplianceResult(
        compliant=all_pass,
        section="Sec 9",
        reason=("all Sec 9 child-processing requirements satisfied" if all_pass
                else f"{len(failed)} Sec 9 requirement(s) failed: " + "; ".join(r.reason for r in failed)),
        citation="DPDP Act 2023, Sec 9",
        sub_results=sub,
    )

"""Sec 8 — General Obligations of Data Fiduciary.

Citation: DPDP Act 2023, Sec 8.
Last updated: 2026-05-23.

This module is not legal advice. It encodes a developer-friendly reading of
DPDP Act 2023 Sec 8 for compliance harness purposes. Consult qualified
counsel before relying on outputs for regulatory or contentious matters.
"""

from __future__ import annotations

from dpdp.exceptions import InvalidInputError, StatuteNotEncodedError
from dpdp.types import BreachRecord, ComplianceResult, ErasureContext

# Draft DPDP Rules 2025 propose notification "without delay" + downstream
# 72-hour follow-up window. v0.1 encodes the 72-hour heuristic; final
# threshold will be calibrated when Rules are notified.
_BREACH_NOTIFY_BOARD_SECONDS = 72 * 3600
_BREACH_NOTIFY_PRINCIPAL_SECONDS = 72 * 3600

_GRIEVANCE_RESPONSE_SECONDS = 30 * 86400  # Sec 8(10) — 30-day heuristic


# ═══════════════════════════════════════════════════════════════════════════
# Sec 8(1) — Data Fiduciary responsible for compliance regardless of agreement
# ═══════════════════════════════════════════════════════════════════════════

def check_fiduciary_accountability(
    has_agreement_to_contrary: bool,
    data_principal_accepts_charge_of_duty: bool,
    processing_undertaken: bool,
    processing_by_processor_on_behalf: bool,
) -> ComplianceResult:
    """Sec 8(1) — Data Fiduciary responsible for compliance irrespective of agreement or charge of duty."""
    sub: list[ComplianceResult] = []

    # Core accountability: fiduciary remains responsible regardless of agreement
    sub.append(ComplianceResult(
        compliant=True,  # accountability is non-delegable by statute
        section="Sec 8(1)",
        reason="Data Fiduciary bears statutory responsibility irrespective of any agreement to the contrary",
        citation="DPDP Act 2023, Sec 8(1)",
    ))

    # When an agreement to the contrary exists, it does not shift responsibility
    if has_agreement_to_contrary:
        sub.append(ComplianceResult(
            compliant=True,
            section="Sec 8(1)",
            reason="agreement to the contrary does not displace Data Fiduciary's statutory responsibility",
            citation="DPDP Act 2023, Sec 8(1)",
        ))

    # Data Principal's acceptance of charge of duty does not relieve fiduciary
    if data_principal_accepts_charge_of_duty:
        sub.append(ComplianceResult(
            compliant=True,
            section="Sec 8(1)",
            reason="Data Principal's acceptance of charge of duty does not relieve Data Fiduciary of responsibility",
            citation="DPDP Act 2023, Sec 8(1)",
        ))

    # Responsibility extends to processing by Data Processor on fiduciary's behalf
    if processing_by_processor_on_behalf:
        sub.append(ComplianceResult(
            compliant=processing_undertaken,
            section="Sec 8(1)",
            reason=("Data Fiduciary responsible for processing undertaken by Data Processor on its behalf"
                    if processing_undertaken
                    else "Data Fiduciary must ensure compliance for processing by Data Processor on its behalf"),
            citation="DPDP Act 2023, Sec 8(1)",
        ))

    all_pass = all(r.compliant for r in sub)
    return ComplianceResult(
        compliant=all_pass,
        section="Sec 8(1)",
        reason=("Data Fiduciary accountability confirmed" if all_pass
                else "; ".join(r.reason for r in sub if not r.compliant)),
        citation="DPDP Act 2023, Sec 8(1)",
        sub_results=sub,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 8(2) — Processor engagement only under valid contract
# ═══════════════════════════════════════════════════════════════════════════

def check_processor_contract(
    processor_engaged: bool,
    has_valid_contract: bool,
) -> ComplianceResult:
    """Sec 8(2) — Data Processor may be engaged only under a valid contract."""
    if not processor_engaged:
        return ComplianceResult(
            compliant=True,
            section="Sec 8(2)",
            reason="no Data Processor engaged — Sec 8(2) not triggered",
            citation="DPDP Act 2023, Sec 8(2)",
        )

    return ComplianceResult(
        compliant=has_valid_contract,
        section="Sec 8(2)",
        reason=("Data Processor engaged under valid contract" if has_valid_contract
                else "Data Processor engaged without a valid contract — Sec 8(2) requires a valid contract"),
        citation="DPDP Act 2023, Sec 8(2)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 8(3) — Accuracy, completeness, consistency when data used for decisions
# ═══════════════════════════════════════════════════════════════════════════

def check_data_accuracy_completeness(
    data_likely_used_for_decision: bool,
    data_is_accurate: bool,
    data_is_complete: bool,
    data_is_consistent: bool,
) -> ComplianceResult:
    """Sec 8(3) — ensure accuracy, completeness and consistency when data likely to be used for a decision."""
    if not data_likely_used_for_decision:
        return ComplianceResult(
            compliant=True,
            section="Sec 8(3)",
            reason="personal data not likely to be used for a decision affecting Data Principal — Sec 8(3) not triggered",
            citation="DPDP Act 2023, Sec 8(3)",
        )

    sub: list[ComplianceResult] = []

    sub.append(ComplianceResult(
        compliant=data_is_accurate,
        section="Sec 8(3)",
        reason=("personal data is accurate" if data_is_accurate
                else "personal data likely used for decision is not accurate"),
        citation="DPDP Act 2023, Sec 8(3)",
    ))

    sub.append(ComplianceResult(
        compliant=data_is_complete,
        section="Sec 8(3)",
        reason=("personal data is complete" if data_is_complete
                else "personal data likely used for decision is not complete"),
        citation="DPDP Act 2023, Sec 8(3)",
    ))

    sub.append(ComplianceResult(
        compliant=data_is_consistent,
        section="Sec 8(3)",
        reason=("personal data is consistent" if data_is_consistent
                else "personal data likely used for decision is not consistent"),
        citation="DPDP Act 2023, Sec 8(3)",
    ))

    all_pass = all(r.compliant for r in sub)
    failed = [r for r in sub if not r.compliant]
    return ComplianceResult(
        compliant=all_pass,
        section="Sec 8(3)",
        reason=("accuracy, completeness and consistency ensured" if all_pass
                else f"{len(failed)} data-quality requirement(s) failed: " + "; ".join(r.reason for r in failed)),
        citation="DPDP Act 2023, Sec 8(3)",
        sub_results=sub,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 8(4) — Technical + organisational measures for compliance
# ═══════════════════════════════════════════════════════════════════════════

def check_compliance_measures(
    has_technical_measures: bool,
    has_organisational_measures: bool,
) -> ComplianceResult:
    """Sec 8(4) — implement appropriate technical and organisational measures for effective compliance."""
    # ambiguity: "appropriate measures" undefined; v0.1 checks presence of both limbs
    sub: list[ComplianceResult] = []

    sub.append(ComplianceResult(
        compliant=has_technical_measures,
        section="Sec 8(4)",
        reason=("appropriate technical measures implemented" if has_technical_measures
                else "appropriate technical measures not implemented for effective compliance"),
        citation="DPDP Act 2023, Sec 8(4)",
    ))

    sub.append(ComplianceResult(
        compliant=has_organisational_measures,
        section="Sec 8(4)",
        reason=("appropriate organisational measures implemented" if has_organisational_measures
                else "appropriate organisational measures not implemented for effective compliance"),
        citation="DPDP Act 2023, Sec 8(4)",
    ))

    all_pass = all(r.compliant for r in sub)
    failed = [r for r in sub if not r.compliant]
    return ComplianceResult(
        compliant=all_pass,
        section="Sec 8(4)",
        reason=("technical and organisational measures in place" if all_pass
                else f"{len(failed)} compliance-measure requirement(s) failed: " + "; ".join(r.reason for r in failed)),
        citation="DPDP Act 2023, Sec 8(4)",
        sub_results=sub,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 8(5) — Reasonable security safeguards to prevent breach (₹250cr penalty)
# ═══════════════════════════════════════════════════════════════════════════

def check_security_safeguards(
    has_technical_safeguards: bool,
    has_organisational_safeguards: bool,
    encrypted_at_rest: bool,
    encrypted_in_transit: bool,
    access_controls_in_place: bool,
    has_incident_response_plan: bool = False,
    has_regular_security_audits: bool = False,
) -> ComplianceResult:
    """Sec 8(5) — reasonable security safeguards to prevent personal data breach."""
    # ambiguity: "reasonable" undefined; v0.1 encodes heuristic dimensions
    # ₹250 cr penalty cap — Schedule Row 1
    sub: list[ComplianceResult] = []

    sub.append(ComplianceResult(
        compliant=has_technical_safeguards,
        section="Sec 8(5)",
        reason=("technical safeguards in place" if has_technical_safeguards
                else "no technical safeguards — firewalls, intrusion detection, endpoint protection not evidenced"),
        citation="DPDP Act 2023, Sec 8(5)",
    ))

    sub.append(ComplianceResult(
        compliant=has_organisational_safeguards,
        section="Sec 8(5)",
        reason=("organisational safeguards in place" if has_organisational_safeguards
                else "no organisational safeguards — security policies, staff training, access-review processes not evidenced"),
        citation="DPDP Act 2023, Sec 8(5)",
    ))

    sub.append(ComplianceResult(
        compliant=encrypted_at_rest,
        section="Sec 8(5)",
        reason=("personal data encrypted at rest" if encrypted_at_rest
                else "personal data not encrypted at rest — unreasonable for ₹250cr penalty exposure"),
        citation="DPDP Act 2023, Sec 8(5)",
    ))

    sub.append(ComplianceResult(
        compliant=encrypted_in_transit,
        section="Sec 8(5)",
        reason=("personal data encrypted in transit" if encrypted_in_transit
                else "personal data not encrypted in transit — unreasonable for ₹250cr penalty exposure"),
        citation="DPDP Act 2023, Sec 8(5)",
    ))

    sub.append(ComplianceResult(
        compliant=access_controls_in_place,
        section="Sec 8(5)",
        reason=("access controls in place" if access_controls_in_place
                else "no access controls — role-based access, least-privilege, MFA not evidenced"),
        citation="DPDP Act 2023, Sec 8(5)",
    ))

    sub.append(ComplianceResult(
        compliant=has_incident_response_plan,
        section="Sec 8(5)",
        reason=("incident response plan exists" if has_incident_response_plan
                else "no incident response plan — unable to contain and notify breaches per Sec 8(6)"),
        citation="DPDP Act 2023, Sec 8(5)",
    ))

    sub.append(ComplianceResult(
        compliant=has_regular_security_audits,
        section="Sec 8(5)",
        reason=("regular security audits conducted" if has_regular_security_audits
                else "no regular security audits — cannot demonstrate ongoing reasonable safeguards"),
        citation="DPDP Act 2023, Sec 8(5)",
    ))

    all_pass = all(r.compliant for r in sub)
    failed = [r for r in sub if not r.compliant]
    return ComplianceResult(
        compliant=all_pass,
        section="Sec 8(5)",
        reason=("reasonable security safeguards in place" if all_pass
                else f"{len(failed)} security-safeguard requirement(s) failed: " + "; ".join(r.reason for r in failed)),
        citation="DPDP Act 2023, Sec 8(5)",
        sub_results=sub,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 8(6) — Breach notification to Board + affected Data Principals (PRESERVED)
# ═══════════════════════════════════════════════════════════════════════════

def check_breach_notification(breach: BreachRecord) -> ComplianceResult:
    """Sec 8(6) — notify Board + affected Data Principals within heuristic 72hr window."""
    if not isinstance(breach, BreachRecord):
        raise InvalidInputError("expected BreachRecord", section="Sec 8(6)")

    sub: list[ComplianceResult] = []

    board_compliant = (
        breach.notified_board_at_unix is not None
        and (breach.notified_board_at_unix - breach.detected_at_unix) <= _BREACH_NOTIFY_BOARD_SECONDS
    )
    sub.append(ComplianceResult(
        compliant=board_compliant,
        section="Sec 8(6)",
        reason=("Board notified within heuristic 72hr window" if board_compliant
                else "Board not notified within 72hr of detection — Sec 8(6) intimation requirement"),
        citation="DPDP Act 2023, Sec 8(6)",
    ))

    principal_compliant = (
        breach.notified_affected_principals_at_unix is not None
        and (breach.notified_affected_principals_at_unix - breach.detected_at_unix) <= _BREACH_NOTIFY_PRINCIPAL_SECONDS
    )
    sub.append(ComplianceResult(
        compliant=principal_compliant,
        section="Sec 8(6)",
        reason=("affected Data Principals notified within heuristic 72hr window" if principal_compliant
                else "affected Data Principals not notified within 72hr of detection"),
        citation="DPDP Act 2023, Sec 8(6)",
    ))

    all_pass = all(r.compliant for r in sub)
    return ComplianceResult(
        compliant=all_pass,
        section="Sec 8(6)",
        reason=("breach notification timely to Board and affected Data Principals" if all_pass
                else "; ".join(r.reason for r in sub if not r.compliant)),
        citation="DPDP Act 2023, Sec 8(6)",
        sub_results=sub,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 8(7)(a) — Erase on consent withdrawal or purpose served
# ═══════════════════════════════════════════════════════════════════════════

def check_erasure_on_withdrawal(erasure: ErasureContext) -> ComplianceResult:
    """Sec 8(7)(a) — erase personal data upon withdrawal or when purpose is no longer served, whichever earlier."""
    if not isinstance(erasure, ErasureContext):
        raise InvalidInputError("expected ErasureContext", section="Sec 8(7)(a)")

    # retention required by law (e.g. Tax / AML) overrides erasure obligation
    if erasure.retention_required_by_law:
        return ComplianceResult(
            compliant=True,
            section="Sec 8(7)(a)",
            reason="retention required under law in force — erasure obligation overridden per Sec 8(7)(a) exception",
            citation="DPDP Act 2023, Sec 8(7)(a)",
        )

    erasure_triggered = erasure.consent_withdrawn or erasure.purpose_served

    if not erasure_triggered:
        return ComplianceResult(
            compliant=True,
            section="Sec 8(7)(a)",
            reason="consent not withdrawn and specified purpose still being served — erasure not yet required",
            citation="DPDP Act 2023, Sec 8(7)(a)",
        )

    return ComplianceResult(
        compliant=erasure.fiduciary_erased,
        section="Sec 8(7)(a)",
        reason=("personal data erased upon withdrawal or purpose served" if erasure.fiduciary_erased
                else "Data Fiduciary failed to erase personal data after consent withdrawal or purpose exhaustion"),
        citation="DPDP Act 2023, Sec 8(7)(a)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 8(7)(b) — Cause Data Processor to erase when Fiduciary erases
# ═══════════════════════════════════════════════════════════════════════════

def check_processor_erasure(erasure: ErasureContext) -> ComplianceResult:
    """Sec 8(7)(b) — cause Data Processor to erase any personal data made available for processing."""
    if not isinstance(erasure, ErasureContext):
        raise InvalidInputError("expected ErasureContext", section="Sec 8(7)(b)")

    # if fiduciary hasn't triggered erasure (retention by law, or no trigger), processor cascade not required
    if erasure.retention_required_by_law:
        return ComplianceResult(
            compliant=True,
            section="Sec 8(7)(b)",
            reason="retention required under law — processor erasure cascade not triggered",
            citation="DPDP Act 2023, Sec 8(7)(b)",
        )

    erasure_triggered = erasure.consent_withdrawn or erasure.purpose_served
    if not erasure_triggered:
        return ComplianceResult(
            compliant=True,
            section="Sec 8(7)(b)",
            reason="erasure not yet required — processor cascade not triggered",
            citation="DPDP Act 2023, Sec 8(7)(b)",
        )

    # if fiduciary has not erased, processor cascade is moot (covered by 8(7)(a) failure)
    if not erasure.fiduciary_erased:
        return ComplianceResult(
            compliant=False,
            section="Sec 8(7)(b)",
            reason="Data Fiduciary has not erased — cannot cause Data Processor to erase data not yet erased at source",
            citation="DPDP Act 2023, Sec 8(7)(b)",
        )

    return ComplianceResult(
        compliant=erasure.processor_erased,
        section="Sec 8(7)(b)",
        reason=("Data Processor caused to erase personal data" if erasure.processor_erased
                else "Data Fiduciary failed to cause its Data Processor to erase personal data made available for processing"),
        citation="DPDP Act 2023, Sec 8(7)(b)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 8(8) — Publish business contact info of DPO / authorised person
# ═══════════════════════════════════════════════════════════════════════════

def check_dpo_contact_publication(
    dpo_contact_published: bool,
    contact_in_prescribed_manner: bool = False,
) -> ComplianceResult:
    """Sec 8(8) — publish business contact information of DPO or authorised person."""
    # delegated to DPDP Rules 2025 — manner prescribed
    sub: list[ComplianceResult] = []

    sub.append(ComplianceResult(
        compliant=dpo_contact_published,
        section="Sec 8(8)",
        reason=("DPO or authorised person business contact information published" if dpo_contact_published
                else "Data Fiduciary must publish business contact information of DPO or person able to answer Data Principal queries"),
        citation="DPDP Act 2023, Sec 8(8)",
    ))

    sub.append(ComplianceResult(
        compliant=contact_in_prescribed_manner,
        section="Sec 8(8)",
        reason=("contact published in prescribed manner" if contact_in_prescribed_manner
                else "contact publication manner not verified against prescribed format — delegated to DPDP Rules 2025"),
        citation="DPDP Act 2023, Sec 8(8)",
    ))

    all_pass = all(r.compliant for r in sub)
    failed = [r for r in sub if not r.compliant]
    return ComplianceResult(
        compliant=all_pass,
        section="Sec 8(8)",
        reason=("DPO contact publication requirements met" if all_pass
                else f"{len(failed)} DPO-contact requirement(s) failed: " + "; ".join(r.reason for r in failed)),
        citation="DPDP Act 2023, Sec 8(8)",
        sub_results=sub,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 8(9) — Establish effective grievance redressal mechanism
# ═══════════════════════════════════════════════════════════════════════════

def check_grievance_mechanism(
    mechanism_established: bool,
    mechanism_is_effective: bool = False,
    mechanism_accessible_to_principals: bool = False,
) -> ComplianceResult:
    """Sec 8(9) — establish an effective mechanism to redress grievances of Data Principals."""
    sub: list[ComplianceResult] = []

    sub.append(ComplianceResult(
        compliant=mechanism_established,
        section="Sec 8(9)",
        reason=("grievance redressal mechanism established" if mechanism_established
                else "Data Fiduciary must establish a grievance redressal mechanism for Data Principals"),
        citation="DPDP Act 2023, Sec 8(9)",
    ))

    sub.append(ComplianceResult(
        compliant=mechanism_is_effective,
        section="Sec 8(9)",
        reason=("mechanism is effective — grievances tracked, escalated and resolved" if mechanism_is_effective
                else "mechanism effectiveness not evidenced — no tracking, escalation or resolution metrics"),
        citation="DPDP Act 2023, Sec 8(9)",
    ))

    sub.append(ComplianceResult(
        compliant=mechanism_accessible_to_principals,
        section="Sec 8(9)",
        reason=("mechanism accessible to Data Principals" if mechanism_accessible_to_principals
                else "mechanism not demonstrably accessible — no public-facing intake channel evidenced"),
        citation="DPDP Act 2023, Sec 8(9)",
    ))

    all_pass = all(r.compliant for r in sub)
    failed = [r for r in sub if not r.compliant]
    return ComplianceResult(
        compliant=all_pass,
        section="Sec 8(9)",
        reason=("effective grievance redressal mechanism established" if all_pass
                else f"{len(failed)} grievance-mechanism requirement(s) failed: " + "; ".join(r.reason for r in failed)),
        citation="DPDP Act 2023, Sec 8(9)",
        sub_results=sub,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 8(10) — Respond to grievances within prescribed period (replaces stub)
# ═══════════════════════════════════════════════════════════════════════════

def check_grievance_redressal(
    grievance_received_at_unix: int,
    grievance_responded_at_unix: int | None,
    resolution_period_days: int = 30,
) -> ComplianceResult:
    """Sec 8(10) — respond to grievances within prescribed period (cross-ref Sec 13(2))."""
    # 30-day heuristic matches existing rights.py — Rules may prescribe different period
    max_seconds = resolution_period_days * 86400

    if grievance_responded_at_unix is None:
        return ComplianceResult(
            compliant=False,
            section="Sec 8(10)",
            reason=f"grievance not responded to within {resolution_period_days}-day prescribed period",
            citation="DPDP Act 2023, Sec 8(10)",
        )

    within_period = (grievance_responded_at_unix - grievance_received_at_unix) <= max_seconds

    return ComplianceResult(
        compliant=within_period,
        section="Sec 8(10)",
        reason=(f"grievance responded to within {resolution_period_days}-day prescribed period" if within_period
                else f"grievance response took longer than {resolution_period_days}-day prescribed period — Sec 8(10) violation"),
        citation="DPDP Act 2023, Sec 8(10)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 8(11) — Central Government may notify additional obligations
# ═══════════════════════════════════════════════════════════════════════════

def check_additional_obligations(
    additional_obligations_notified: list[str] | None = None,
    all_obligations_complied: bool = True,
) -> ComplianceResult:
    """Sec 8(11) — Central Government may, by notification, impose additional obligations on Data Fiduciaries."""
    obligations = additional_obligations_notified or []

    if not obligations:
        return ComplianceResult(
            compliant=True,
            section="Sec 8(11)",
            reason="no additional obligations notified by Central Government — Sec 8(11) not triggered",
            citation="DPDP Act 2023, Sec 8(11)",
        )

    return ComplianceResult(
        compliant=all_obligations_complied,
        section="Sec 8(11)",
        reason=(f"all {len(obligations)} notified additional obligation(s) complied with" if all_obligations_complied
                else f"{len(obligations)} additional obligation(s) notified by Central Govt — not all complied with"),
        citation="DPDP Act 2023, Sec 8(11)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Master compliance aggregator — Sec 8(1) through 8(11)
# ═══════════════════════════════════════════════════════════════════════════

def check_fiduciary_compliance(
    # Sec 8(1) — accountability
    has_agreement_to_contrary: bool = False,
    data_principal_accepts_charge_of_duty: bool = False,
    processing_undertaken: bool = True,
    processing_by_processor_on_behalf: bool = False,
    # Sec 8(2) — processor contract
    processor_engaged: bool = False,
    has_valid_processor_contract: bool = False,
    # Sec 8(3) — data quality
    data_likely_used_for_decision: bool = False,
    data_is_accurate: bool = True,
    data_is_complete: bool = True,
    data_is_consistent: bool = True,
    # Sec 8(4) — compliance measures
    has_technical_measures: bool = True,
    has_organisational_measures: bool = True,
    # Sec 8(5) — security safeguards
    has_technical_safeguards: bool = True,
    has_organisational_safeguards: bool = True,
    encrypted_at_rest: bool = True,
    encrypted_in_transit: bool = True,
    access_controls_in_place: bool = True,
    has_incident_response_plan: bool = False,
    has_regular_security_audits: bool = False,
    # Sec 8(7) — erasure
    erasure: ErasureContext | None = None,
    # Sec 8(8) — DPO contact
    dpo_contact_published: bool = True,
    contact_in_prescribed_manner: bool = False,
    # Sec 8(9) — grievance mechanism
    grievance_mechanism_established: bool = True,
    grievance_mechanism_effective: bool = False,
    grievance_mechanism_accessible: bool = False,
    # Sec 8(10) — grievance response
    grievance_received_at_unix: int = 0,
    grievance_responded_at_unix: int | None = 0,
    grievance_resolution_period_days: int = 30,
    # Sec 8(11) — additional obligations
    additional_obligations_notified: list[str] | None = None,
    all_additional_obligations_complied: bool = True,
) -> ComplianceResult:
    """Sec 8 — master compliance check aggregating obligations under DPDP Act 2023, Sec 8(1)-(11)."""
    sub: list[ComplianceResult] = []

    # Sec 8(1)
    sub.append(check_fiduciary_accountability(
        has_agreement_to_contrary=has_agreement_to_contrary,
        data_principal_accepts_charge_of_duty=data_principal_accepts_charge_of_duty,
        processing_undertaken=processing_undertaken,
        processing_by_processor_on_behalf=processing_by_processor_on_behalf,
    ))

    # Sec 8(2)
    sub.append(check_processor_contract(
        processor_engaged=processor_engaged,
        has_valid_contract=has_valid_processor_contract,
    ))

    # Sec 8(3)
    sub.append(check_data_accuracy_completeness(
        data_likely_used_for_decision=data_likely_used_for_decision,
        data_is_accurate=data_is_accurate,
        data_is_complete=data_is_complete,
        data_is_consistent=data_is_consistent,
    ))

    # Sec 8(4)
    sub.append(check_compliance_measures(
        has_technical_measures=has_technical_measures,
        has_organisational_measures=has_organisational_measures,
    ))

    # Sec 8(5)
    sub.append(check_security_safeguards(
        has_technical_safeguards=has_technical_safeguards,
        has_organisational_safeguards=has_organisational_safeguards,
        encrypted_at_rest=encrypted_at_rest,
        encrypted_in_transit=encrypted_in_transit,
        access_controls_in_place=access_controls_in_place,
        has_incident_response_plan=has_incident_response_plan,
        has_regular_security_audits=has_regular_security_audits,
    ))

    # Sec 8(7)(a) + 8(7)(b)
    if erasure is not None:
        sub.append(check_erasure_on_withdrawal(erasure))
        sub.append(check_processor_erasure(erasure))

    # Sec 8(8)
    sub.append(check_dpo_contact_publication(
        dpo_contact_published=dpo_contact_published,
        contact_in_prescribed_manner=contact_in_prescribed_manner,
    ))

    # Sec 8(9)
    sub.append(check_grievance_mechanism(
        mechanism_established=grievance_mechanism_established,
        mechanism_is_effective=grievance_mechanism_effective,
        mechanism_accessible_to_principals=grievance_mechanism_accessible,
    ))

    # Sec 8(10)
    sub.append(check_grievance_redressal(
        grievance_received_at_unix=grievance_received_at_unix,
        grievance_responded_at_unix=grievance_responded_at_unix,
        resolution_period_days=grievance_resolution_period_days,
    ))

    # Sec 8(11)
    sub.append(check_additional_obligations(
        additional_obligations_notified=additional_obligations_notified,
        all_obligations_complied=all_additional_obligations_complied,
    ))

    all_pass = all(r.compliant for r in sub)
    failed = [r for r in sub if not r.compliant]
    return ComplianceResult(
        compliant=all_pass,
        section="Sec 8",
        reason=("All Sec 8(1)-(11) fiduciary obligations met" if all_pass
                else f"{len(failed)} Sec 8 obligation(s) failed: " + "; ".join(r.reason for r in failed)),
        citation="DPDP Act 2023, Sec 8",
        sub_results=sub,
    )

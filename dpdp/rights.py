"""Sec 11-14 — Rights of Data Principal.

Citation: DPDP Act 2023, Sec 11, 12, 13, 14.
Last updated: 2026-05-23.

Sec 11 — Right to access information about personal data.
Sec 12 — Right to correction, completion, updating, and erasure.
Sec 13 — Right of grievance redressal.
Sec 14 — Right to nominate.

Draft DPDP Rules 2025 contemplate response timelines — v0.1 uses a 30-day
heuristic for grievance resolution until DPDP Rules are notified.

This module is not legal advice. It encodes a developer-friendly reading of
DPDP Act 2023 Sec 11-14 for compliance harness purposes. Consult qualified
counsel before relying on outputs for regulatory or contentious matters.
"""

from __future__ import annotations

from dpdp.exceptions import InvalidInputError
from dpdp.types import ComplianceResult, RightsRequest, RightType

# REQUIRES NEW DATACLASS IN dpdp/types.py:
#   AccessDisclosure with fields: summary_provided: bool, processing_activities_disclosed: bool,
#     identities_listed: bool, generic_third_party_label_used: bool,
#     description_of_shared_data_provided: bool, other_prescribed_info_provided: bool
#
# REQUIRES NEW DATACLASS IN dpdp/types.py:
#   CorrectionContext with fields: correction_requested: bool, completion_requested: bool,
#     updating_requested: bool, erasure_requested: bool, correction_provided: bool,
#     completion_provided: bool, updating_provided: bool, erasure_provided: bool,
#     data_was_inaccurate_or_misleading: bool, data_was_incomplete: bool,
#     retention_required_by_law: bool, retention_necessary_for_purpose: bool


# ═══════════════════════════════════════════════════════════════════════════
# preserved existing helpers
# ═══════════════════════════════════════════════════════════════════════════

def _section_for(right: RightType) -> str:
    return {
        RightType.ACCESS_AND_INFORMATION: "Sec 11",
        RightType.CORRECTION_AND_ERASURE: "Sec 12",
        RightType.GRIEVANCE_REDRESSAL: "Sec 13",
        RightType.NOMINATION: "Sec 14",
    }[right]


def _citation_for(right: RightType) -> str:
    return f"DPDP Act 2023, {_section_for(right)}"


def check_rights_response(request: RightsRequest) -> ComplianceResult:
    """Validate that a rights request was responded to within the prescribed window."""
    if not isinstance(request, RightsRequest):
        raise InvalidInputError("expected RightsRequest", section="Sec 11-14")

    if request.responded_at_unix is None:
        return ComplianceResult(
            compliant=False,
            section=_section_for(request.right),
            reason="no response recorded; rights request unanswered",
            citation=_citation_for(request.right),
        )

    elapsed_days = (request.responded_at_unix - request.received_at_unix) / 86400
    deadline = float(request.grievance_resolution_period_days)
    compliant = elapsed_days <= deadline

    return ComplianceResult(
        compliant=compliant,
        section=_section_for(request.right),
        reason=(
            f"responded in {elapsed_days:.1f} days (within {deadline:.0f}-day window)"
            if compliant
            else f"responded in {elapsed_days:.1f} days — exceeds {deadline:.0f}-day window"
        ),
        citation=_citation_for(request.right),
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 11 — Right to access information about personal data
# ═══════════════════════════════════════════════════════════════════════════

def check_sec_11_1_a_summary(summary_provided: bool, processing_activities_disclosed: bool) -> ComplianceResult:
    """Sec 11(1)(a) — right to obtain summary of personal data + processing activities."""
    compliant = summary_provided and processing_activities_disclosed
    return ComplianceResult(
        compliant=compliant,
        section="Sec 11(1)(a)",
        reason=(
            "summary of personal data and processing activities provided"
            if compliant
            else _missing_11_1_a_reason(summary_provided, processing_activities_disclosed)
        ),
        citation="DPDP Act 2023, Sec 11(1)(a)",
    )


def _missing_11_1_a_reason(summary_provided: bool, processing_activities_disclosed: bool) -> str:
    missing: list[str] = []
    if not summary_provided:
        missing.append("summary of personal data not provided")
    if not processing_activities_disclosed:
        missing.append("processing activities not disclosed")
    return "; ".join(missing)


def check_sec_11_1_b_identities(identities_listed: bool, generic_third_party_label_used: bool) -> ComplianceResult:
    """Sec 11(1)(b) — right to identities of Fiduciaries/Processors with whom data shared."""
    if not identities_listed:
        return ComplianceResult(
            compliant=False,
            section="Sec 11(1)(b)",
            reason="identities of Data Fiduciaries/Processors with whom data shared not listed",
            citation="DPDP Act 2023, Sec 11(1)(b)",
        )
    if generic_third_party_label_used:
        return ComplianceResult(
            compliant=False,
            section="Sec 11(1)(b)",
            reason="generic third-party label used instead of specific identities — Sec 11(1)(b) requires specific identities of each Data Fiduciary/Processor",
            citation="DPDP Act 2023, Sec 11(1)(b)",
        )
    return ComplianceResult(
        compliant=True,
        section="Sec 11(1)(b)",
        reason="specific identities of Data Fiduciaries/Processors listed",
        citation="DPDP Act 2023, Sec 11(1)(b)",
    )


def check_sec_11_1_b_description(description_of_shared_data_provided: bool) -> ComplianceResult:
    """Sec 11(1)(b) — right to description of data shared with other Fiduciaries/Processors."""
    return ComplianceResult(
        compliant=description_of_shared_data_provided,
        section="Sec 11(1)(b)",
        reason=(
            "description of shared data provided"
            if description_of_shared_data_provided
            else "description of data shared with other Fiduciaries/Processors not provided"
        ),
        citation="DPDP Act 2023, Sec 11(1)(b)",
    )


def check_sec_11_1_c_other_info(other_prescribed_info_provided: bool) -> ComplianceResult:
    """Sec 11(1)(c) — right to other prescribed information related to processing."""
    # delegated to DPDP Rules 2025 — manner prescribed
    return ComplianceResult(
        compliant=other_prescribed_info_provided,
        section="Sec 11(1)(c)",
        reason=(
            "other prescribed processing information provided"
            if other_prescribed_info_provided
            else "other prescribed information related to processing not provided"
        ),
        citation="DPDP Act 2023, Sec 11(1)(c)",
    )


def check_sec_11_2_law_enforcement_exemption(sharing_authorised_by_law: bool) -> ComplianceResult:
    """Sec 11(2) — 11(1)(b)/(c) do not apply to sharing authorised by law."""
    return ComplianceResult(
        compliant=True,
        section="Sec 11(2)",
        reason=(
            "sharing authorised by law — Sec 11(1)(b)/(c) disclosure obligations do not apply"
            if sharing_authorised_by_law
            else "sharing not authorised by law; Sec 11(1)(b)/(c) disclosure obligations apply — exemption not available for voluntary sharing"
        ),
        citation="DPDP Act 2023, Sec 11(2)",
    )


def check_sec_11(
    summary_provided: bool,
    processing_activities_disclosed: bool,
    identities_listed: bool,
    generic_third_party_label_used: bool,
    description_of_shared_data_provided: bool,
    other_prescribed_info_provided: bool,
    sharing_authorised_by_law: bool,
) -> ComplianceResult:
    """Sec 11 — master aggregator for right to access information about personal data."""
    sub_results: list[ComplianceResult] = []

    sub_results.append(check_sec_11_1_a_summary(summary_provided, processing_activities_disclosed))

    if sharing_authorised_by_law:
        sub_results.append(ComplianceResult(
            compliant=True,
            section="Sec 11(1)(b)",
            reason="identities not disclosed per Sec 11(2) — sharing authorised by law",
            citation="DPDP Act 2023, Sec 11(1)(b)",
        ))
        sub_results.append(ComplianceResult(
            compliant=True,
            section="Sec 11(1)(b)",
            reason="description of shared data not disclosed per Sec 11(2) — sharing authorised by law",
            citation="DPDP Act 2023, Sec 11(1)(b)",
        ))
        sub_results.append(ComplianceResult(
            compliant=True,
            section="Sec 11(1)(c)",
            reason="other prescribed info not disclosed per Sec 11(2) — sharing authorised by law",
            citation="DPDP Act 2023, Sec 11(1)(c)",
        ))
    else:
        sub_results.append(check_sec_11_1_b_identities(identities_listed, generic_third_party_label_used))
        sub_results.append(check_sec_11_1_b_description(description_of_shared_data_provided))
        sub_results.append(check_sec_11_1_c_other_info(other_prescribed_info_provided))

    sub_results.append(check_sec_11_2_law_enforcement_exemption(sharing_authorised_by_law))

    all_compliant = all(r.compliant for r in sub_results)
    return ComplianceResult(
        compliant=all_compliant,
        section="Sec 11",
        reason=(
            "all Sec 11 access-right obligations satisfied"
            if all_compliant
            else "one or more Sec 11 access-right obligations not satisfied"
        ),
        citation="DPDP Act 2023, Sec 11",
        sub_results=sub_results,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 12 — Right to correction, completion, updating, and erasure
# ═══════════════════════════════════════════════════════════════════════════

def check_sec_12_1_correction(correction_requested: bool, correction_provided: bool) -> ComplianceResult:
    """Sec 12(1) — right to correction of personal data."""
    if not correction_requested:
        return ComplianceResult(
            compliant=True,
            section="Sec 12(1)",
            reason="correction not requested — right not exercised",
            citation="DPDP Act 2023, Sec 12(1)",
        )
    return ComplianceResult(
        compliant=correction_provided,
        section="Sec 12(1)",
        reason=(
            "correction of personal data provided"
            if correction_provided
            else "correction of personal data requested but not provided"
        ),
        citation="DPDP Act 2023, Sec 12(1)",
    )


def check_sec_12_1_completion(completion_requested: bool, completion_provided: bool) -> ComplianceResult:
    """Sec 12(1) — right to completion of incomplete personal data."""
    if not completion_requested:
        return ComplianceResult(
            compliant=True,
            section="Sec 12(1)",
            reason="completion not requested — right not exercised",
            citation="DPDP Act 2023, Sec 12(1)",
        )
    return ComplianceResult(
        compliant=completion_provided,
        section="Sec 12(1)",
        reason=(
            "completion of incomplete personal data provided"
            if completion_provided
            else "completion of incomplete personal data requested but not provided"
        ),
        citation="DPDP Act 2023, Sec 12(1)",
    )


def check_sec_12_1_updating(updating_requested: bool, updating_provided: bool) -> ComplianceResult:
    """Sec 12(1) — right to updating of personal data."""
    if not updating_requested:
        return ComplianceResult(
            compliant=True,
            section="Sec 12(1)",
            reason="updating not requested — right not exercised",
            citation="DPDP Act 2023, Sec 12(1)",
        )
    return ComplianceResult(
        compliant=updating_provided,
        section="Sec 12(1)",
        reason=(
            "updating of personal data provided"
            if updating_provided
            else "updating of personal data requested but not provided"
        ),
        citation="DPDP Act 2023, Sec 12(1)",
    )


def check_sec_12_1_erasure(erasure_requested: bool, erasure_provided: bool, retention_required_by_law: bool = False, retention_necessary_for_purpose: bool = False) -> ComplianceResult:
    """Sec 12(1) — right to erasure of personal data."""
    if not erasure_requested:
        return ComplianceResult(
            compliant=True,
            section="Sec 12(1)",
            reason="erasure not requested — right not exercised",
            citation="DPDP Act 2023, Sec 12(1)",
        )
    if erasure_provided:
        return ComplianceResult(
            compliant=True,
            section="Sec 12(1)",
            reason="erasure of personal data carried out",
            citation="DPDP Act 2023, Sec 12(1)",
        )
    if retention_required_by_law:
        return ComplianceResult(
            compliant=True,
            section="Sec 12(1)",
            reason="erasure not carried out — retention required by law (lawful exception under Sec 12(3))",
            citation="DPDP Act 2023, Sec 12(1)",
        )
    if retention_necessary_for_purpose:
        return ComplianceResult(
            compliant=True,
            section="Sec 12(1)",
            reason="erasure not carried out — retention necessary for specified purpose (lawful exception under Sec 12(3))",
            citation="DPDP Act 2023, Sec 12(1)",
        )
    return ComplianceResult(
        compliant=False,
        section="Sec 12(1)",
        reason="erasure of personal data requested but not carried out — no lawful retention exception applies",
        citation="DPDP Act 2023, Sec 12(1)",
    )


def check_sec_12_2_a_correction_duty(correction_requested: bool, fiduciary_corrected: bool, data_was_inaccurate_or_misleading: bool) -> ComplianceResult:
    """Sec 12(2)(a) — Fiduciary must correct inaccurate/misleading data on request."""
    if not correction_requested:
        return ComplianceResult(
            compliant=True,
            section="Sec 12(2)(a)",
            reason="correction not requested — no fiduciary duty triggered",
            citation="DPDP Act 2023, Sec 12(2)(a)",
        )
    if not data_was_inaccurate_or_misleading:
        return ComplianceResult(
            compliant=True,
            section="Sec 12(2)(a)",
            reason="data was not inaccurate or misleading — no correction duty triggered",
            citation="DPDP Act 2023, Sec 12(2)(a)",
        )
    return ComplianceResult(
        compliant=fiduciary_corrected,
        section="Sec 12(2)(a)",
        reason=(
            "Fiduciary corrected inaccurate/misleading personal data as required"
            if fiduciary_corrected
            else "Fiduciary failed to correct inaccurate/misleading personal data on request"
        ),
        citation="DPDP Act 2023, Sec 12(2)(a)",
    )


def check_sec_12_2_b_completion_duty(completion_requested: bool, fiduciary_completed: bool, data_was_incomplete: bool) -> ComplianceResult:
    """Sec 12(2)(b) — Fiduciary must complete incomplete data on request."""
    if not completion_requested:
        return ComplianceResult(
            compliant=True,
            section="Sec 12(2)(b)",
            reason="completion not requested — no fiduciary duty triggered",
            citation="DPDP Act 2023, Sec 12(2)(b)",
        )
    if not data_was_incomplete:
        return ComplianceResult(
            compliant=True,
            section="Sec 12(2)(b)",
            reason="data was not incomplete — no completion duty triggered",
            citation="DPDP Act 2023, Sec 12(2)(b)",
        )
    return ComplianceResult(
        compliant=fiduciary_completed,
        section="Sec 12(2)(b)",
        reason=(
            "Fiduciary completed incomplete personal data as required"
            if fiduciary_completed
            else "Fiduciary failed to complete incomplete personal data on request"
        ),
        citation="DPDP Act 2023, Sec 12(2)(b)",
    )


def check_sec_12_2_c_updating_duty(updating_requested: bool, fiduciary_updated: bool) -> ComplianceResult:
    """Sec 12(2)(c) — Fiduciary must update personal data on request."""
    if not updating_requested:
        return ComplianceResult(
            compliant=True,
            section="Sec 12(2)(c)",
            reason="updating not requested — no fiduciary duty triggered",
            citation="DPDP Act 2023, Sec 12(2)(c)",
        )
    return ComplianceResult(
        compliant=fiduciary_updated,
        section="Sec 12(2)(c)",
        reason=(
            "Fiduciary updated personal data as required"
            if fiduciary_updated
            else "Fiduciary failed to update personal data on request"
        ),
        citation="DPDP Act 2023, Sec 12(2)(c)",
    )


def check_sec_12_3_erasure_duty(erasure_requested: bool, fiduciary_erased: bool, retention_required_by_law: bool, retention_necessary_for_purpose: bool) -> ComplianceResult:
    """Sec 12(3) — Fiduciary must erase on request unless retention required by law or necessary for specified purpose."""
    if not erasure_requested:
        return ComplianceResult(
            compliant=True,
            section="Sec 12(3)",
            reason="erasure not requested — no fiduciary duty triggered",
            citation="DPDP Act 2023, Sec 12(3)",
        )
    if fiduciary_erased:
        return ComplianceResult(
            compliant=True,
            section="Sec 12(3)",
            reason="Fiduciary erased personal data on request",
            citation="DPDP Act 2023, Sec 12(3)",
        )
    if retention_required_by_law:
        return ComplianceResult(
            compliant=True,
            section="Sec 12(3)",
            reason="erasure not carried out — retention required by law (lawful exception under Sec 12(3))",
            citation="DPDP Act 2023, Sec 12(3)",
        )
    if retention_necessary_for_purpose:
        return ComplianceResult(
            compliant=True,
            section="Sec 12(3)",
            reason="erasure not carried out — retention necessary for specified purpose (lawful exception under Sec 12(3))",
            citation="DPDP Act 2023, Sec 12(3)",
        )
    return ComplianceResult(
        compliant=False,
        section="Sec 12(3)",
        reason="Fiduciary failed to erase personal data on request — no lawful retention exception applies",
        citation="DPDP Act 2023, Sec 12(3)",
    )


def check_sec_12(
    correction_requested: bool,
    correction_provided: bool,
    completion_requested: bool,
    completion_provided: bool,
    updating_requested: bool,
    updating_provided: bool,
    erasure_requested: bool,
    erasure_provided: bool,
    data_was_inaccurate_or_misleading: bool,
    data_was_incomplete: bool,
    retention_required_by_law: bool,
    retention_necessary_for_purpose: bool,
) -> ComplianceResult:
    """Sec 12 — master aggregator for correction, completion, updating, and erasure rights."""
    sub_results: list[ComplianceResult] = [
        check_sec_12_1_correction(correction_requested, correction_provided),
        check_sec_12_1_completion(completion_requested, completion_provided),
        check_sec_12_1_updating(updating_requested, updating_provided),
        check_sec_12_1_erasure(erasure_requested, erasure_provided, retention_required_by_law, retention_necessary_for_purpose),
        check_sec_12_2_a_correction_duty(correction_requested, correction_provided, data_was_inaccurate_or_misleading),
        check_sec_12_2_b_completion_duty(completion_requested, completion_provided, data_was_incomplete),
        check_sec_12_2_c_updating_duty(updating_requested, updating_provided),
        check_sec_12_3_erasure_duty(erasure_requested, erasure_provided, retention_required_by_law, retention_necessary_for_purpose),
    ]

    all_compliant = all(r.compliant for r in sub_results)
    return ComplianceResult(
        compliant=all_compliant,
        section="Sec 12",
        reason=(
            "all Sec 12 correction/erasure obligations satisfied"
            if all_compliant
            else "one or more Sec 12 correction/erasure obligations not satisfied"
        ),
        citation="DPDP Act 2023, Sec 12",
        sub_results=sub_results,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 13 — Right of grievance redressal
# ═══════════════════════════════════════════════════════════════════════════

def check_sec_13_1_mechanism_available(mechanism_available: bool) -> ComplianceResult:
    """Sec 13(1) — readily available means of grievance redressal provided by Fiduciary or Consent Manager."""
    return ComplianceResult(
        compliant=mechanism_available,
        section="Sec 13(1)",
        reason=(
            "readily available means of grievance redressal provided"
            if mechanism_available
            else "no readily available means of grievance redressal provided by Fiduciary or Consent Manager"
        ),
        citation="DPDP Act 2023, Sec 13(1)",
    )


def check_sec_13_2_response_period(request: RightsRequest) -> ComplianceResult:
    """Sec 13(2) — Fiduciary must respond to grievance within prescribed period."""
    if not isinstance(request, RightsRequest):
        raise InvalidInputError("expected RightsRequest", section="Sec 13(2)")
    if request.right != RightType.GRIEVANCE_REDRESSAL:
        raise InvalidInputError(
            "RightsRequest.right must be GRIEVANCE_REDRESSAL for Sec 13(2) check",
            section="Sec 13(2)",
        )

    if request.responded_at_unix is None:
        return ComplianceResult(
            compliant=False,
            section="Sec 13(2)",
            reason="no response recorded; grievance unanswered",
            citation="DPDP Act 2023, Sec 13(2)",
        )

    elapsed_days = (request.responded_at_unix - request.received_at_unix) / 86400
    deadline = float(request.grievance_resolution_period_days)
    compliant = elapsed_days <= deadline

    return ComplianceResult(
        compliant=compliant,
        section="Sec 13(2)",
        reason=(
            f"grievance responded in {elapsed_days:.1f} days (within {deadline:.0f}-day window)"
            if compliant
            else f"grievance responded in {elapsed_days:.1f} days — exceeds {deadline:.0f}-day window"
        ),
        citation="DPDP Act 2023, Sec 13(2)",
    )


def check_sec_13_3_exhaustion_required(grievance_filed_with_fiduciary_first: bool) -> ComplianceResult:
    """Sec 13(3) — Data Principal must exhaust internal grievance mechanism before approaching Board."""
    return ComplianceResult(
        compliant=grievance_filed_with_fiduciary_first,
        section="Sec 13(3)",
        reason=(
            "grievance filed with Fiduciary/Consent Manager first — exhaustion requirement satisfied"
            if grievance_filed_with_fiduciary_first
            else "Data Principal must exhaust internal grievance mechanism before approaching Board — fiduciary-level grievance not filed first"
        ),
        citation="DPDP Act 2023, Sec 13(3)",
    )


def check_sec_13(
    mechanism_available: bool,
    request: RightsRequest,
    grievance_filed_with_fiduciary_first: bool,
) -> ComplianceResult:
    """Sec 13 — master aggregator for grievance redressal rights."""
    if not isinstance(request, RightsRequest):
        raise InvalidInputError("expected RightsRequest", section="Sec 13")

    sub_results: list[ComplianceResult] = [
        check_sec_13_1_mechanism_available(mechanism_available),
        check_sec_13_2_response_period(request),
        check_sec_13_3_exhaustion_required(grievance_filed_with_fiduciary_first),
    ]

    all_compliant = all(r.compliant for r in sub_results)
    return ComplianceResult(
        compliant=all_compliant,
        section="Sec 13",
        reason=(
            "all Sec 13 grievance-redressal obligations satisfied"
            if all_compliant
            else "one or more Sec 13 grievance-redressal obligations not satisfied"
        ),
        citation="DPDP Act 2023, Sec 13",
        sub_results=sub_results,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 14 — Right to nominate
# ═══════════════════════════════════════════════════════════════════════════

def check_sec_14_1_nomination(nominee_designated: bool, manner_prescribed_followed: bool) -> ComplianceResult:
    """Sec 14(1) — right to nominate another individual to exercise rights in case of death/incapacity."""
    # delegated to DPDP Rules 2025 — manner prescribed
    compliant = nominee_designated and manner_prescribed_followed
    if not nominee_designated:
        return ComplianceResult(
            compliant=False,
            section="Sec 14(1)",
            reason="no nominee designated for exercising rights in case of death/incapacity",
            citation="DPDP Act 2023, Sec 14(1)",
        )
    if not manner_prescribed_followed:
        return ComplianceResult(
            compliant=False,
            section="Sec 14(1)",
            reason="nominee designated but manner prescribed not followed — Sec 14 requires nomination in prescribed manner",  # delegated to DPDP Rules 2025 — manner prescribed
            citation="DPDP Act 2023, Sec 14(1)",
        )
    return ComplianceResult(
        compliant=True,
        section="Sec 14(1)",
        reason="nominee designated in prescribed manner for exercising rights in case of death/incapacity",
        citation="DPDP Act 2023, Sec 14(1)",
    )


def check_sec_14_2_incapacity_definition(incapacity_meets_definition: bool) -> ComplianceResult:
    """Sec 14(2) — definition of incapacity for nomination purposes (death, mental incapacity, persistent vegetative state, etc.)."""
    return ComplianceResult(
        compliant=incapacity_meets_definition,
        section="Sec 14(2)",
        reason=(
            "incapacity meets statutory definition for nomination purposes"
            if incapacity_meets_definition
            else "claimed incapacity does not meet statutory definition (death, mental incapacity, persistent vegetative state, or equivalent) for nomination purposes"
        ),
        citation="DPDP Act 2023, Sec 14(2)",
    )


def check_sec_14(
    nominee_designated: bool,
    manner_prescribed_followed: bool,
    incapacity_meets_definition: bool,
) -> ComplianceResult:
    """Sec 14 — master aggregator for nomination rights."""
    sub_results: list[ComplianceResult] = [
        check_sec_14_1_nomination(nominee_designated, manner_prescribed_followed),
        check_sec_14_2_incapacity_definition(incapacity_meets_definition),
    ]

    all_compliant = all(r.compliant for r in sub_results)
    return ComplianceResult(
        compliant=all_compliant,
        section="Sec 14",
        reason=(
            "all Sec 14 nomination obligations satisfied"
            if all_compliant
            else "one or more Sec 14 nomination obligations not satisfied"
        ),
        citation="DPDP Act 2023, Sec 14",
        sub_results=sub_results,
    )

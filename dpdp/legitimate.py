"""Sec 7 — Certain Legitimate Uses.

Citation: DPDP Act 2023, Sec 7.
Last updated: 2026-05-23.

DPDP enumerates 9 EXHAUSTIVE legitimate uses as alternatives to consent.
There is NO general "legitimate interests" ground (cf. GDPR Art 6(1)(f)).
Construction must be narrow.

This module is not legal advice. It encodes a developer-friendly reading of
DPDP Act 2023 Sec 7 for compliance harness purposes. Consult qualified
counsel before relying on outputs for regulatory or contentious matters.
"""

from __future__ import annotations

from dpdp.exceptions import InvalidInputError
from dpdp.types import ComplianceResult, LegitimateUseCase, LegitimateUseRecord

# Sec 7 is the DPDP-vs-GDPR wedge — list is EXHAUSTIVE; no analogue of GDPR Art 6(1)(f) 'legitimate interests'.

# ═══════════════════════════════════════════════════════════════════════════
# REQUIRES ENUM UPDATE IN dpdp/types.py: LegitimateUseCase members must be:
# ═══════════════════════════════════════════════════════════════════════════
#
#   VOLUNTARY_PROVISION_FOR_SPECIFIED_PURPOSE = "sec_7_a"
#   STATE_SUBSIDY_BENEFIT_SERVICE_LICENSE     = "sec_7_b"
#   STATE_FUNCTION_UNDER_LAW                  = "sec_7_c"
#   LEGAL_DISCLOSURE_TO_STATE                 = "sec_7_d"
#   COURT_JUDGMENT_COMPLIANCE                 = "sec_7_e"
#   MEDICAL_EMERGENCY                         = "sec_7_f"
#   EPIDEMIC_PUBLIC_HEALTH_EMERGENCY          = "sec_7_g"
#   DISASTER_OR_BREAKDOWN_OF_PUBLIC_ORDER     = "sec_7_h"
#   EMPLOYMENT_PURPOSES                       = "sec_7_i"
#
# Remove: PERFORMANCE_OF_LAW_OR_JUDGMENT (replaced by 7(c), 7(d), 7(e)).
#
# ═══════════════════════════════════════════════════════════════════════════
# PROPOSED LegitimateUseRecord FIELD ADDITIONS (dpdp/types.py):
# ═══════════════════════════════════════════════════════════════════════════
#
#   purpose_matches_voluntary_provision: bool = False   # Sec 7(a) narrow guard
#   has_prior_consent_for_state_subsidy: bool = False    # Sec 7(b)(i)
#   data_from_notified_database: bool = False            # Sec 7(b)(ii)
#   has_statutory_disclosure_obligation: bool = False    # Sec 7(d)
#   has_judgment_or_order: bool = False                  # Sec 7(e)
#   is_government_health_measure: bool = False           # Sec 7(g)
#   is_government_disaster_measure: bool = False         # Sec 7(h)
#   is_employer_employee_relationship: bool = False      # Sec 7(i) narrow guard
#
# Until these are added, standalone check_() functions accept them as
# direct parameters. The master dispatcher passes conservative defaults.


# ═══════════════════════════════════════════════════════════════════════════
# Sec 7(a) — Voluntary provision for specified purpose
# ═══════════════════════════════════════════════════════════════════════════

def check_sec_7_a(
    is_personal_data_voluntarily_provided: bool,
    purpose_matches_voluntary_provision: bool = True,
) -> ComplianceResult:
    """Sec 7(a) — Data Principal voluntarily provided personal data for the specified purpose and has not indicated non-consent."""
    if not is_personal_data_voluntarily_provided:
        return ComplianceResult(
            compliant=False,
            section="Sec 7(a)",
            reason="Sec 7(a) requires Data Principal to have voluntarily provided personal data for the specified purpose",
            citation="DPDP Act 2023, Sec 7(a)",
        )
    if not purpose_matches_voluntary_provision:
        return ComplianceResult(
            compliant=False,
            section="Sec 7(a)",
            reason="Sec 7(a) requires the processing purpose to match the purpose for which Data Principal voluntarily provided data",
            citation="DPDP Act 2023, Sec 7(a)",
        )
    return ComplianceResult(
        compliant=True,
        section="Sec 7(a)",
        reason="personal data voluntarily provided by Data Principal for the specified purpose",
        citation="DPDP Act 2023, Sec 7(a)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 7(b) — State subsidy / benefit / service / certificate / licence / permit
# ═══════════════════════════════════════════════════════════════════════════

def check_sec_7_b_i(
    is_state_function: bool,
    has_prior_consent: bool = False,
) -> ComplianceResult:
    """Sec 7(b)(i) — State subsidy/benefit: Data Principal previously consented to processing for subsidy, benefit, service, certificate, licence or permit."""
    if not is_state_function:
        return ComplianceResult(
            compliant=False,
            section="Sec 7(b)(i)",
            reason="Sec 7(b)(i) limited to State and instrumentalities; private parties cannot invoke",
            citation="DPDP Act 2023, Sec 7(b)(i)",
        )
    if not has_prior_consent:
        return ComplianceResult(
            compliant=False,
            section="Sec 7(b)(i)",
            reason="Sec 7(b)(i) requires Data Principal to have previously given consent to processing for a subsidy, benefit, service, certificate, licence or permit",
            citation="DPDP Act 2023, Sec 7(b)(i)",
        )
    return ComplianceResult(
        compliant=True,
        section="Sec 7(b)(i)",
        reason="Data Principal previously consented to processing by State for subsidy, benefit, service, certificate, licence or permit",
        citation="DPDP Act 2023, Sec 7(b)(i)",
    )


def check_sec_7_b_ii(
    is_state_function: bool,
    data_from_notified_database: bool = False,
) -> ComplianceResult:
    """Sec 7(b)(ii) — State subsidy/benefit: personal data available in digital form from notified database, register or surplus maintained by State."""
    if not is_state_function:
        return ComplianceResult(
            compliant=False,
            section="Sec 7(b)(ii)",
            reason="Sec 7(b)(ii) limited to State and instrumentalities; private parties cannot invoke",
            citation="DPDP Act 2023, Sec 7(b)(ii)",
        )
    if not data_from_notified_database:
        return ComplianceResult(
            compliant=False,
            section="Sec 7(b)(ii)",
            reason="Sec 7(b)(ii) requires personal data to be available in digital form from a database, register or surplus maintained by State and notified by Central Government",
            citation="DPDP Act 2023, Sec 7(b)(ii)",
        )
    return ComplianceResult(
        compliant=True,
        section="Sec 7(b)(ii)",
        reason="personal data available in digital form from notified State-maintained database, register or surplus",
        citation="DPDP Act 2023, Sec 7(b)(ii)",
    )


def check_sec_7_b(
    is_state_function: bool,
    has_prior_consent: bool = False,
    data_from_notified_database: bool = False,
) -> ComplianceResult:
    """Sec 7(b) — State subsidy / benefit / service / certificate / licence / permit (umbrella with sub-clauses (i) and (ii))."""
    if not is_state_function:
        return ComplianceResult(
            compliant=False,
            section="Sec 7(b)",
            reason="Sec 7(b) limited to State and instrumentalities; private parties cannot invoke",
            citation="DPDP Act 2023, Sec 7(b)",
        )

    sub_i = check_sec_7_b_i(is_state_function=is_state_function, has_prior_consent=has_prior_consent)
    sub_ii = check_sec_7_b_ii(is_state_function=is_state_function, data_from_notified_database=data_from_notified_database)

    # Sec 7(b) satisfied if EITHER sub-clause (i) OR (ii) pathway is met
    either_pathway = sub_i.compliant or sub_ii.compliant
    return ComplianceResult(
        compliant=either_pathway,
        section="Sec 7(b)",
        reason=("State subsidy/benefit/service/certificate/licence/permit — at least one pathway satisfied"
                if either_pathway
                else "Sec 7(b) requires either prior consent pathway (i) or notified-database pathway (ii) — neither satisfied"),
        citation="DPDP Act 2023, Sec 7(b)",
        sub_results=[sub_i, sub_ii],
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 7(c) — State function under law / sovereignty / integrity / security
# ═══════════════════════════════════════════════════════════════════════════

def check_sec_7_c(is_state_function: bool) -> ComplianceResult:
    """Sec 7(c) — performance by State of any function under law or in interest of sovereignty, integrity or security of India."""
    if not is_state_function:
        return ComplianceResult(
            compliant=False,
            section="Sec 7(c)",
            reason="Sec 7(c) limited to State and instrumentalities performing functions under law; private parties cannot invoke",
            citation="DPDP Act 2023, Sec 7(c)",
        )
    return ComplianceResult(
        compliant=True,
        section="Sec 7(c)",
        reason="State function under law or in interest of sovereignty, integrity or security of India",
        citation="DPDP Act 2023, Sec 7(c)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 7(d) — Legal disclosure to State
# ═══════════════════════════════════════════════════════════════════════════

def check_sec_7_d(has_statutory_disclosure_obligation: bool) -> ComplianceResult:
    """Sec 7(d) — disclosure to State or instrumentality under statutory obligation; voluntary disclosure does not qualify."""
    if not has_statutory_disclosure_obligation:
        return ComplianceResult(
            compliant=False,
            section="Sec 7(d)",
            reason="Sec 7(d) requires a statutory obligation to disclose information to the State; voluntary or contractual disclosure does not qualify",
            citation="DPDP Act 2023, Sec 7(d)",
        )
    return ComplianceResult(
        compliant=True,
        section="Sec 7(d)",
        reason="disclosure to State or instrumentality under obligation imposed by law in force in India",
        citation="DPDP Act 2023, Sec 7(d)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 7(e) — Court judgment or order compliance
# ═══════════════════════════════════════════════════════════════════════════

def check_sec_7_e(has_judgment_or_order: bool) -> ComplianceResult:
    """Sec 7(e) — compliance with judgment or order issued under any law, including foreign contractual/civil judgments."""
    if not has_judgment_or_order:
        return ComplianceResult(
            compliant=False,
            section="Sec 7(e)",
            reason="Sec 7(e) requires an actual judgment, order or decree of a court or tribunal; mere threat of litigation does not qualify",
            citation="DPDP Act 2023, Sec 7(e)",
        )
    return ComplianceResult(
        compliant=True,
        section="Sec 7(e)",
        reason="processing for compliance with judgment or order of court, tribunal, or foreign contractual/civil judgment",
        citation="DPDP Act 2023, Sec 7(e)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 7(f) — Medical emergency
# ═══════════════════════════════════════════════════════════════════════════

def check_sec_7_f(threatens_life_or_health: bool) -> ComplianceResult:
    """Sec 7(f) — responding to a medical emergency involving threat to life or direct threat to health of Data Principal or any other individual."""
    if not threatens_life_or_health:
        return ComplianceResult(
            compliant=False,
            section="Sec 7(f)",
            reason="Sec 7(f) requires an actual medical emergency involving threat to life or direct threat to health; routine healthcare does not qualify",
            citation="DPDP Act 2023, Sec 7(f)",
        )
    return ComplianceResult(
        compliant=True,
        section="Sec 7(f)",
        reason="processing for response to medical emergency involving threat to life or direct threat to health",
        citation="DPDP Act 2023, Sec 7(f)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 7(g) — Epidemic / outbreak / public health threat
# ═══════════════════════════════════════════════════════════════════════════

def check_sec_7_g(is_government_health_measure: bool) -> ComplianceResult:
    """Sec 7(g) — medical treatment or health services during epidemic, outbreak of disease or threat to public health; government-level intervention only."""
    if not is_government_health_measure:
        return ComplianceResult(
            compliant=False,
            section="Sec 7(g)",
            reason="Sec 7(g) requires government-level health intervention during epidemic, outbreak or public health threat; private marketing or commercial health services do not qualify",
            citation="DPDP Act 2023, Sec 7(g)",
        )
    return ComplianceResult(
        compliant=True,
        section="Sec 7(g)",
        reason="government measures to provide medical treatment or health services during epidemic, outbreak of disease or threat to public health",
        citation="DPDP Act 2023, Sec 7(g)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 7(h) — Disaster / breakdown of public order
# ═══════════════════════════════════════════════════════════════════════════

def check_sec_7_h(is_government_disaster_measure: bool) -> ComplianceResult:
    """Sec 7(h) — measures to ensure safety or provide assistance during disaster or breakdown of public order; government measures only."""
    if not is_government_disaster_measure:
        return ComplianceResult(
            compliant=False,
            section="Sec 7(h)",
            reason="Sec 7(h) requires government measures for safety or assistance during disaster or breakdown of public order; private initiatives do not qualify",
            citation="DPDP Act 2023, Sec 7(h)",
        )
    return ComplianceResult(
        compliant=True,
        section="Sec 7(h)",
        reason="government measures to ensure safety of, or provide assistance to, individuals during disaster or breakdown of public order",
        citation="DPDP Act 2023, Sec 7(h)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 7(i) — Employment purposes
# ═══════════════════════════════════════════════════════════════════════════

def check_sec_7_i(
    is_employment_related: bool,
    is_employer_employee_relationship: bool = False,
) -> ComplianceResult:
    """Sec 7(i) — employment purposes: requires employer-employee relationship; contractors, prospects, customers do not qualify."""
    if not is_employment_related:
        return ComplianceResult(
            compliant=False,
            section="Sec 7(i)",
            reason="Sec 7(i) limited to employment context; processing unrelated to employment does not qualify",
            citation="DPDP Act 2023, Sec 7(i)",
        )
    if not is_employer_employee_relationship:
        return ComplianceResult(
            compliant=False,
            section="Sec 7(i)",
            reason="Sec 7(i) requires an employer-employee relationship; contractors, job applicants, prospects and customers do not qualify",
            citation="DPDP Act 2023, Sec 7(i)",
        )
    return ComplianceResult(
        compliant=True,
        section="Sec 7(i)",
        reason="processing for employment purposes — safeguarding employer from loss or liability, or providing service or benefit to employee",
        citation="DPDP Act 2023, Sec 7(i)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Master dispatcher — check_legitimate_use(LegitimateUseRecord)
# ═══════════════════════════════════════════════════════════════════════════

def check_legitimate_use(record: LegitimateUseRecord) -> ComplianceResult:
    """Sec 7 — validate a processing activity asserted under one of the 9 exhaustive legitimate uses."""
    if not isinstance(record, LegitimateUseRecord):
        raise InvalidInputError("expected LegitimateUseRecord", section="Sec 7")

    case = record.asserted_case

    if case == LegitimateUseCase.VOLUNTARY_PROVISION_FOR_SPECIFIED_PURPOSE:
        return check_sec_7_a(
            is_personal_data_voluntarily_provided=record.is_personal_data_voluntarily_provided,
            # PROPOSED FIELD: purpose_matches_voluntary_provision — defaults True until field added to record
        )

    if case == LegitimateUseCase.STATE_SUBSIDY_BENEFIT_SERVICE_LICENSE:
        return check_sec_7_b(
            is_state_function=record.is_state_function,
            # PROPOSED FIELDS: has_prior_consent_for_state_subsidy, data_from_notified_database — default False
        )

    if hasattr(LegitimateUseCase, 'STATE_FUNCTION_UNDER_LAW') and case == LegitimateUseCase.STATE_FUNCTION_UNDER_LAW:
        return check_sec_7_c(is_state_function=record.is_state_function)

    if hasattr(LegitimateUseCase, 'LEGAL_DISCLOSURE_TO_STATE') and case == LegitimateUseCase.LEGAL_DISCLOSURE_TO_STATE:
        return check_sec_7_d(
            # PROPOSED FIELD: has_statutory_disclosure_obligation — use has_other_lawful_basis as weak proxy
            has_statutory_disclosure_obligation=record.has_other_lawful_basis,
        )

    if hasattr(LegitimateUseCase, 'COURT_JUDGMENT_COMPLIANCE') and case == LegitimateUseCase.COURT_JUDGMENT_COMPLIANCE:
        return check_sec_7_e(
            # PROPOSED FIELD: has_judgment_or_order — use has_other_lawful_basis as weak proxy
            has_judgment_or_order=record.has_other_lawful_basis,
        )

    if case == LegitimateUseCase.MEDICAL_EMERGENCY:
        return check_sec_7_f(threatens_life_or_health=record.threatens_life_or_health)

    if case == LegitimateUseCase.EPIDEMIC_PUBLIC_HEALTH_EMERGENCY:
        return check_sec_7_g(
            # PROPOSED FIELD: is_government_health_measure — default False until field added
            is_government_health_measure=False,
        )

    if case == LegitimateUseCase.DISASTER_OR_BREAKDOWN_OF_PUBLIC_ORDER:
        return check_sec_7_h(
            # PROPOSED FIELD: is_government_disaster_measure — default False until field added
            is_government_disaster_measure=False,
        )

    if case == LegitimateUseCase.EMPLOYMENT_PURPOSES:
        return check_sec_7_i(
            is_employment_related=record.is_employment_related,
            # PROPOSED FIELD: is_employer_employee_relationship — defaults False (narrow construction)
        )

    return ComplianceResult(
        compliant=False,
        section="Sec 7",
        reason=f"unrecognised legitimate-use case: {case}",
        citation="DPDP Act 2023, Sec 7",
    )

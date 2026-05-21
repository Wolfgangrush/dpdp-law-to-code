"""Sec 10 — Significant Data Fiduciary.

Citation: DPDP Act 2023, Sec 10.
Last updated: 2026-05-23.

Sec 10(1) — Central Govt notifies an entity as SDF based on six factors:
    (a) volume + sensitivity of personal data processed
    (b) risk to rights of Data Principals
    (c) potential impact on sovereignty + integrity of India
    (d) risk to electoral democracy
    (e) security of the State
    (f) public order

Sec 10(2) — SDF additional obligations: DPO (India-based, accountable to
Board of Directors, grievance contact), independent data auditor, periodic
DPIA + audits, other prescribed measures.

This module is not legal advice. It encodes a developer-friendly reading of
DPDP Act 2023 Sec 10 for compliance harness purposes. Consult qualified
counsel before relying on outputs for regulatory or contentious matters.
"""

from __future__ import annotations

from dpdp.exceptions import InvalidInputError, StatuteNotEncodedError
from dpdp.types import ComplianceResult, SDFContext

# TODO v0.2 — expand SDFContext (dpdp/types.py) with per-sub-clause fields
# below and drop the getattr(…) proxy fallbacks used in this module:
#
#   dpo_represents_sdf_under_act: bool = False        # Sec 10(2)(a)(i)
#   dpo_based_in_india: bool = False                   # Sec 10(2)(a)(ii)
#   dpo_accountable_to_board: bool = False             # Sec 10(2)(a)(iii)
#   dpo_is_grievance_contact: bool = False             # Sec 10(2)(a)(iv)
#   conducts_periodic_audit: bool = False              # Sec 10(2)(c)(ii)
#   complies_with_other_prescribed_measures: bool = False  # Sec 10(2)(d)
#
# Until then, this module reads each sub-clause via getattr() with a
# documented proxy fallback (typically has_appointed_dpo).

_THRESHOLD_HEURISTIC = 0.6  # self-assessment aid — only Central Govt notification under Sec 10(1) is binding
_FACTOR_THRESHOLD = 0.5  # per-factor elevated-risk threshold for 10(1)(a)-(f) individual checks


def _validate_context(context: SDFContext) -> None:
    if not isinstance(context, SDFContext):
        raise InvalidInputError("expected SDFContext", section="Sec 10")


# ═══════════════════════════════════════════════════════════════════════════
# Sec 10(1)(a) — volume + sensitivity of personal data processed
# ═══════════════════════════════════════════════════════════════════════════

def check_sec_10_1_a(context: SDFContext) -> ComplianceResult:
    """Sec 10(1)(a) — volume and sensitivity of personal data processed."""
    _validate_context(context)

    volume_signal = min(1.0, context.volume_of_personal_data_processed / 10_000_000)
    combined = max(volume_signal, context.sensitivity_of_personal_data)
    elevated = combined >= _FACTOR_THRESHOLD

    return ComplianceResult(
        compliant=not elevated,
        section="Sec 10(1)(a)",
        reason=(
            f"volume signal {volume_signal:.2f}, sensitivity {context.sensitivity_of_personal_data:.2f} — "
            f"combined {combined:.2f} >= {_FACTOR_THRESHOLD} — elevated SDF concern"
            if elevated
            else f"volume signal {volume_signal:.2f}, sensitivity {context.sensitivity_of_personal_data:.2f} — "
                 f"combined {combined:.2f} < {_FACTOR_THRESHOLD} — not an elevated concern"
        ),
        citation="DPDP Act 2023, Sec 10(1)(a)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 10(1)(b) — risk to rights of Data Principal
# ═══════════════════════════════════════════════════════════════════════════

def check_sec_10_1_b(context: SDFContext) -> ComplianceResult:
    """Sec 10(1)(b) — risk to the rights of Data Principal."""
    _validate_context(context)

    risk = context.risk_to_rights_of_data_principals
    elevated = risk >= _FACTOR_THRESHOLD

    return ComplianceResult(
        compliant=not elevated,
        section="Sec 10(1)(b)",
        reason=(
            f"risk to rights of Data Principals {risk:.2f} >= {_FACTOR_THRESHOLD} — elevated SDF concern"
            if elevated
            else f"risk to rights of Data Principals {risk:.2f} < {_FACTOR_THRESHOLD} — not an elevated concern"
        ),
        citation="DPDP Act 2023, Sec 10(1)(b)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 10(1)(c) — potential impact on sovereignty + integrity of India
# ═══════════════════════════════════════════════════════════════════════════

def check_sec_10_1_c(context: SDFContext) -> ComplianceResult:
    """Sec 10(1)(c) — potential impact on the sovereignty and integrity of India."""
    _validate_context(context)

    risk = context.risk_to_sovereignty_or_integrity
    elevated = risk >= _FACTOR_THRESHOLD

    return ComplianceResult(
        compliant=not elevated,
        section="Sec 10(1)(c)",
        reason=(
            f"risk to sovereignty/integrity {risk:.2f} >= {_FACTOR_THRESHOLD} — elevated SDF concern"
            if elevated
            else f"risk to sovereignty/integrity {risk:.2f} < {_FACTOR_THRESHOLD} — not an elevated concern"
        ),
        citation="DPDP Act 2023, Sec 10(1)(c)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 10(1)(d) — risk to electoral democracy
# ═══════════════════════════════════════════════════════════════════════════

def check_sec_10_1_d(context: SDFContext) -> ComplianceResult:
    """Sec 10(1)(d) — risk to electoral democracy."""
    _validate_context(context)

    risk = context.risk_to_electoral_democracy
    elevated = risk >= _FACTOR_THRESHOLD

    return ComplianceResult(
        compliant=not elevated,
        section="Sec 10(1)(d)",
        reason=(
            f"risk to electoral democracy {risk:.2f} >= {_FACTOR_THRESHOLD} — elevated SDF concern"
            if elevated
            else f"risk to electoral democracy {risk:.2f} < {_FACTOR_THRESHOLD} — not an elevated concern"
        ),
        citation="DPDP Act 2023, Sec 10(1)(d)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 10(1)(e) — security of the State
# ═══════════════════════════════════════════════════════════════════════════

def check_sec_10_1_e(context: SDFContext) -> ComplianceResult:
    """Sec 10(1)(e) — security of the State."""
    _validate_context(context)

    risk = context.risk_to_state_security
    elevated = risk >= _FACTOR_THRESHOLD

    return ComplianceResult(
        compliant=not elevated,
        section="Sec 10(1)(e)",
        reason=(
            f"risk to State security {risk:.2f} >= {_FACTOR_THRESHOLD} — elevated SDF concern"
            if elevated
            else f"risk to State security {risk:.2f} < {_FACTOR_THRESHOLD} — not an elevated concern"
        ),
        citation="DPDP Act 2023, Sec 10(1)(e)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 10(1)(f) — public order
# ═══════════════════════════════════════════════════════════════════════════

def check_sec_10_1_f(context: SDFContext) -> ComplianceResult:
    """Sec 10(1)(f) — public order."""
    _validate_context(context)

    risk = context.risk_to_public_order
    elevated = risk >= _FACTOR_THRESHOLD

    return ComplianceResult(
        compliant=not elevated,
        section="Sec 10(1)(f)",
        reason=(
            f"risk to public order {risk:.2f} >= {_FACTOR_THRESHOLD} — elevated SDF concern"
            if elevated
            else f"risk to public order {risk:.2f} < {_FACTOR_THRESHOLD} — not an elevated concern"
        ),
        citation="DPDP Act 2023, Sec 10(1)(f)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 10(1) — composite SDF threshold assessment (aggregates (a)-(f))
# ═══════════════════════════════════════════════════════════════════════════

def assess_sdf_threshold(context: SDFContext) -> ComplianceResult:
    """Sec 10(1) — heuristic SDF-likelihood assessment aggregating six Central-Govt-assessed criteria."""
    _validate_context(context)

    # collect individual factor checks as sub-results
    sub: list[ComplianceResult] = []
    sub.append(check_sec_10_1_a(context))
    sub.append(check_sec_10_1_b(context))
    sub.append(check_sec_10_1_c(context))
    sub.append(check_sec_10_1_d(context))
    sub.append(check_sec_10_1_e(context))
    sub.append(check_sec_10_1_f(context))

    if context.notified_as_sdf_by_central_govt:
        return ComplianceResult(
            compliant=True,
            section="Sec 10(1)",
            reason="entity has been notified by Central Govt as a Significant Data Fiduciary",
            citation="DPDP Act 2023, Sec 10(1)",
            sub_results=sub,
        )

    volume_signal = min(1.0, context.volume_of_personal_data_processed / 10_000_000)
    composite = (
        0.20 * volume_signal
        + 0.20 * context.sensitivity_of_personal_data
        + 0.20 * context.risk_to_rights_of_data_principals
        + 0.10 * context.risk_to_sovereignty_or_integrity
        + 0.10 * context.risk_to_electoral_democracy
        + 0.10 * context.risk_to_state_security
        + 0.10 * context.risk_to_public_order
    )

    likely = composite >= _THRESHOLD_HEURISTIC
    return ComplianceResult(
        compliant=not likely,
        section="Sec 10(1)",
        reason=(
            f"heuristic SDF-likelihood score {composite:.2f} >= {_THRESHOLD_HEURISTIC} — prepare SDF obligations; only Central Govt notification is binding"
            if likely
            else f"heuristic SDF-likelihood score {composite:.2f} < {_THRESHOLD_HEURISTIC} — likely not SDF; continue monitoring volume + sensitivity"
        ),
        citation="DPDP Act 2023, Sec 10(1)",
        sub_results=sub,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 10(2)(a) — SDF shall appoint a Data Protection Officer
# ═══════════════════════════════════════════════════════════════════════════

def check_sec_10_2_a_dpo(context: SDFContext) -> ComplianceResult:
    """Sec 10(2)(a) — appoint DPO who represents SDF, is based in India, accountable to Board, and is grievance contact."""
    _validate_context(context)

    sub: list[ComplianceResult] = []

    # Sec 10(2)(a)(i) — DPO represents SDF under the Act
    # proxy: has_appointed_dpo until dpo_represents_sdf_under_act is added to SDFContext
    dpo_represents = getattr(context, 'dpo_represents_sdf_under_act', context.has_appointed_dpo)
    sub.append(ComplianceResult(
        compliant=dpo_represents,
        section="Sec 10(2)(a)(i)",
        reason=("DPO represents SDF under the provisions of this Act" if dpo_represents
                else "Sec 10(2)(a)(i) requires DPO to represent the SDF under the provisions of this Act"),
        citation="DPDP Act 2023, Sec 10(2)(a)(i)",
    ))

    # Sec 10(2)(a)(ii) — DPO based in India
    # proxy: has_appointed_dpo until dpo_based_in_india is added to SDFContext
    dpo_in_india = getattr(context, 'dpo_based_in_india', context.has_appointed_dpo)
    sub.append(ComplianceResult(
        compliant=dpo_in_india,
        section="Sec 10(2)(a)(ii)",
        reason=("DPO based in India" if dpo_in_india
                else "Sec 10(2)(a)(ii) requires DPO to be based in India — ₹150 crore penalty exposure"),
        citation="DPDP Act 2023, Sec 10(2)(a)(ii)",
    ))

    # Sec 10(2)(a)(iii) — DPO accountable to Board of Directors
    # proxy: has_appointed_dpo until dpo_accountable_to_board is added to SDFContext
    dpo_accountable = getattr(context, 'dpo_accountable_to_board', context.has_appointed_dpo)
    sub.append(ComplianceResult(
        compliant=dpo_accountable,
        section="Sec 10(2)(a)(iii)",
        reason=("DPO is an individual responsible to the Board of Directors or similar governing body"
                if dpo_accountable
                else "Sec 10(2)(a)(iii) requires DPO to be responsible to the Board of Directors or similar governing body"),
        citation="DPDP Act 2023, Sec 10(2)(a)(iii)",
    ))

    # Sec 10(2)(a)(iv) — DPO is point of contact for grievance redressal
    # proxy: has_appointed_dpo until dpo_is_grievance_contact is added to SDFContext
    dpo_grievance = getattr(context, 'dpo_is_grievance_contact', context.has_appointed_dpo)
    sub.append(ComplianceResult(
        compliant=dpo_grievance,
        section="Sec 10(2)(a)(iv)",
        reason=("DPO is the point of contact for the grievance redressal mechanism"
                if dpo_grievance
                else "Sec 10(2)(a)(iv) requires DPO to be the point of contact for the grievance redressal mechanism"),
        citation="DPDP Act 2023, Sec 10(2)(a)(iv)",
    ))

    all_pass = all(r.compliant for r in sub)
    failed = [r for r in sub if not r.compliant]
    return ComplianceResult(
        compliant=all_pass,
        section="Sec 10(2)(a)",
        reason=("all DPO appointment requirements satisfied" if all_pass
                else f"{len(failed)} DPO requirement(s) failed: " + "; ".join(r.reason for r in failed)),
        citation="DPDP Act 2023, Sec 10(2)(a)",
        sub_results=sub,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 10(2)(b) — SDF shall appoint an independent data auditor
# ═══════════════════════════════════════════════════════════════════════════

def check_sec_10_2_b_auditor(context: SDFContext) -> ComplianceResult:
    """Sec 10(2)(b) — appoint an independent data auditor to evaluate compliance with the Act."""
    _validate_context(context)

    return ComplianceResult(
        compliant=context.has_appointed_data_auditor,
        section="Sec 10(2)(b)",
        reason=("independent data auditor appointed to evaluate compliance with the Act"
                if context.has_appointed_data_auditor
                else "Sec 10(2)(b) requires SDF to appoint an independent data auditor who shall evaluate compliance"),
        citation="DPDP Act 2023, Sec 10(2)(b)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 10(2)(c) — periodic DPIA + periodic audit + other prescribed measures
# ═══════════════════════════════════════════════════════════════════════════

def check_sec_10_2_c_dpia(context: SDFContext) -> ComplianceResult:
    """Sec 10(2)(c) — undertake periodic Data Protection Impact Assessment and periodic audit."""
    _validate_context(context)

    sub: list[ComplianceResult] = []

    # Sec 10(2)(c)(i) — periodic DPIA
    sub.append(ComplianceResult(
        compliant=context.conducts_periodic_dpia,
        section="Sec 10(2)(c)(i)",
        reason=("periodic Data Protection Impact Assessment undertaken"
                if context.conducts_periodic_dpia
                else "Sec 10(2)(c)(i) requires SDF to undertake periodic Data Protection Impact Assessment"),
        citation="DPDP Act 2023, Sec 10(2)(c)(i)",
    ))

    # Sec 10(2)(c)(ii) — periodic audit
    # proxy: conducts_periodic_dpia until conducts_periodic_audit is added to SDFContext
    periodic_audit = getattr(context, 'conducts_periodic_audit', context.conducts_periodic_dpia)
    sub.append(ComplianceResult(
        compliant=periodic_audit,
        section="Sec 10(2)(c)(ii)",
        reason=("periodic audit undertaken" if periodic_audit
                else "Sec 10(2)(c)(ii) requires SDF to undertake periodic audit"),
        citation="DPDP Act 2023, Sec 10(2)(c)(ii)",
    ))

    # Sec 10(2)(c)(iii) — such other measures as may be prescribed
    # delegated to DPDP Rules 2025 — manner prescribed
    sub.append(ComplianceResult(
        compliant=True,
        section="Sec 10(2)(c)(iii)",
        reason="other measures as may be prescribed — delegated to DPDP Rules 2025; no measure currently notified",
        citation="DPDP Act 2023, Sec 10(2)(c)(iii)",
    ))

    all_pass = all(r.compliant for r in sub)
    failed = [r for r in sub if not r.compliant]
    return ComplianceResult(
        compliant=all_pass,
        section="Sec 10(2)(c)",
        reason=("periodic DPIA, audit, and other prescribed measures undertaken" if all_pass
                else f"{len(failed)} DPIA/audit requirement(s) failed: " + "; ".join(r.reason for r in failed)),
        citation="DPDP Act 2023, Sec 10(2)(c)",
        sub_results=sub,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 10(2)(d) — other measures including such other measures as prescribed
# ═══════════════════════════════════════════════════════════════════════════

def check_sec_10_2_d_other_measures(context: SDFContext) -> ComplianceResult:
    """Sec 10(2)(d) — other measures as may be prescribed (catch-all delegation to Rules)."""
    _validate_context(context)

    # proxy: complies_with_other_prescribed_measures if the field exists, else True
    # delegated to DPDP Rules 2025 — manner prescribed
    other_complied = getattr(context, 'complies_with_other_prescribed_measures', True)

    return ComplianceResult(
        compliant=other_complied,
        section="Sec 10(2)(d)",
        reason=("other prescribed measures complied with — delegated to DPDP Rules 2025" if other_complied
                else "Sec 10(2)(d) requires SDF to undertake other measures as may be prescribed — delegated to DPDP Rules 2025"),
        citation="DPDP Act 2023, Sec 10(2)(d)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 10(2) — composite SDF obligations aggregator (a)-(d)
# ═══════════════════════════════════════════════════════════════════════════

def check_sdf_obligations(context: SDFContext) -> ComplianceResult:
    """Sec 10(2) — validate SDF obligations: DPO, auditor, DPIA, other measures."""
    _validate_context(context)

    sub: list[ComplianceResult] = []
    sub.append(check_sec_10_2_a_dpo(context))
    sub.append(check_sec_10_2_b_auditor(context))
    sub.append(check_sec_10_2_c_dpia(context))
    sub.append(check_sec_10_2_d_other_measures(context))

    all_pass = all(r.compliant for r in sub)
    failed = [r for r in sub if not r.compliant]
    return ComplianceResult(
        compliant=all_pass,
        section="Sec 10(2)",
        reason=("all SDF obligations satisfied" if all_pass
                else f"{len(failed)} SDF obligation(s) failed: " + "; ".join(r.reason for r in failed)),
        citation="DPDP Act 2023, Sec 10(2)",
        sub_results=sub,
    )

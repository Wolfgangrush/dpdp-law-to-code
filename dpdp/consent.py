"""Sec 6 — Consent.

Citation: DPDP Act 2023, Sec 6.
Last updated: 2026-05-21.

This module is not legal advice. It encodes a developer-friendly reading of
DPDP Act 2023 Sec 6 for compliance harness purposes. Consult qualified
counsel before relying on outputs for regulatory or contentious matters.
"""

from __future__ import annotations

from dpdp.exceptions import InvalidInputError
from dpdp.types import ComplianceResult, ConsentRecord

_F_S_I_U_U = (
    ("is_free", "Free", "consent not coerced or pressured"),
    ("is_specific", "Specific", "consent limited to the specified purpose"),
    ("is_informed", "Informed", "Data Principal was given Sec 5 notice"),
    (
        "is_unconditional",
        "Unconditional",
        "consent not made conditional on unrelated terms",
    ),
    ("is_unambiguous", "Unambiguous", "consent is unmistakable in scope"),
)


def check_consent(consent: ConsentRecord) -> ComplianceResult:
    """Sec 6(1)-(4) — master consent validation: F-S-I-U-U + language + withdrawal."""
    if not isinstance(consent, ConsentRecord):
        raise InvalidInputError("expected ConsentRecord", section="Sec 6")

    sub: list[ComplianceResult] = []

    # Sec 6(1) — F-S-I-U-U
    for attr, label, requirement in _F_S_I_U_U:
        present = bool(getattr(consent, attr))
        sub.append(
            ComplianceResult(
                compliant=present,
                section="Sec 6(1)",
                reason=(
                    f"{label}: satisfied"
                    if present
                    else f"{label}: not satisfied — {requirement}"
                ),
                citation="DPDP Act 2023, Sec 6(1)",
            )
        )

    # Sec 6(1) — clear affirmative action
    sub.append(
        ComplianceResult(
            compliant=consent.has_clear_affirmative_action,
            section="Sec 6(1)",
            reason=(
                "clear affirmative action present"
                if consent.has_clear_affirmative_action
                else "no clear affirmative action — pre-ticked boxes / silence do not constitute consent"
            ),
            citation="DPDP Act 2023, Sec 6(1)",
        )
    )

    # Sec 6(1) — no pre-checked boxes
    sub.append(
        ComplianceResult(
            compliant=not consent.is_pre_checked,
            section="Sec 6(1)",
            reason=(
                "not pre-checked"
                if not consent.is_pre_checked
                else "pre-checked checkbox defeats clear affirmative action requirement"
            ),
            citation="DPDP Act 2023, Sec 6(1)",
        )
    )

    # Sec 6(1) — limited to specified purpose
    sub.append(
        ComplianceResult(
            compliant=consent.is_limited_to_specified_purpose,
            section="Sec 6(1)",
            reason=(
                "limited to specified purpose"
                if consent.is_limited_to_specified_purpose
                else "consent must be limited to specified purpose"
            ),
            citation="DPDP Act 2023, Sec 6(1)",
        )
    )

    # Sec 6(1) — not bundled with unrelated terms
    sub.append(
        ComplianceResult(
            compliant=not consent.is_bundled_with_unrelated_terms,
            section="Sec 6(1)",
            reason=(
                "not bundled with unrelated terms"
                if not consent.is_bundled_with_unrelated_terms
                else "bundled consent invalid to the extent of infringement"
            ),
            citation="DPDP Act 2023, Sec 6(1)",
        )
    )

    # Sec 6(2) — infringing consent invalid
    sub.append(
        ComplianceResult(
            compliant=not consent.has_infringing_provision,
            section="Sec 6(2)",
            reason=(
                "no infringing provision"
                if not consent.has_infringing_provision
                else "consent contains provision infringing the Act, rules, or other law — invalid to that extent"
            ),
            citation="DPDP Act 2023, Sec 6(2)",
        )
    )

    # Sec 6(3) — clear/plain language
    sub.append(
        ComplianceResult(
            compliant=consent.request_in_clear_plain_language,
            section="Sec 6(3)",
            reason=(
                "consent request in clear and plain language"
                if consent.request_in_clear_plain_language
                else "consent request must be in clear and plain language"
            ),
            citation="DPDP Act 2023, Sec 6(3)",
        )
    )

    # Sec 6(3) — Eighth Schedule language option
    sub.append(
        ComplianceResult(
            compliant=consent.has_eighth_schedule_language_option,
            section="Sec 6(3)",
            reason=(
                "Eighth Schedule language option given"
                if consent.has_eighth_schedule_language_option
                else "must provide option to access request in English or Eighth Schedule language"
            ),
            citation="DPDP Act 2023, Sec 6(3)",
        )
    )

    # Sec 6(3) — DPO contact
    sub.append(
        ComplianceResult(
            compliant=consent.dpo_contact_provided,
            section="Sec 6(3)",
            reason=(
                "DPO or authorised person contact provided"
                if consent.dpo_contact_provided
                else "must provide DPO contact details for exercise of Data Principal rights"
            ),
            citation="DPDP Act 2023, Sec 6(3)",
        )
    )

    # Sec 6(4) — withdrawal as easy as giving
    sub.append(
        ComplianceResult(
            compliant=consent.is_withdrawable_easily,
            section="Sec 6(4)",
            reason=(
                "withdrawal as easy as giving consent"
                if consent.is_withdrawable_easily
                else "withdrawal must be as easy as the original act of giving consent"
            ),
            citation="DPDP Act 2023, Sec 6(4)",
        )
    )

    all_pass = all(r.compliant for r in sub)
    failed = [r for r in sub if not r.compliant]
    return ComplianceResult(
        compliant=all_pass,
        section="Sec 6",
        reason=(
            "All Sec 6(1)-(4) consent requirements met"
            if all_pass
            else f"{len(failed)} requirement(s) failed: "
            + "; ".join(r.reason for r in failed)
        ),
        citation="DPDP Act 2023, Sec 6",
        sub_results=sub,
    )


def check_withdrawal_ease(consent: ConsentRecord) -> ComplianceResult:
    """Sec 6(4) — right to withdraw consent, as easy as giving."""
    return ComplianceResult(
        compliant=consent.is_withdrawable_easily,
        section="Sec 6(4)",
        reason=(
            "withdrawal as easy as grant"
            if consent.is_withdrawable_easily
            else "withdrawal harder than grant — Sec 6(4) violation"
        ),
        citation="DPDP Act 2023, Sec 6(4)",
    )


def check_infringing_consent(has_infringing_provision: bool) -> ComplianceResult:
    """Sec 6(2) — infringing consent invalid to extent of infringement."""
    return ComplianceResult(
        compliant=not has_infringing_provision,
        section="Sec 6(2)",
        reason=(
            "no infringing provision"
            if not has_infringing_provision
            else "any part of consent that infringes the Act, rules, or other law is invalid to that extent"
        ),
        citation="DPDP Act 2023, Sec 6(2)",
    )


def check_consent_request_presentation(
    clear_plain_language: bool,
    eighth_schedule_option: bool,
    dpo_contact_provided: bool,
) -> ComplianceResult:
    """Sec 6(3) — consent request in clear/plain language, Eighth Schedule option, DPO contact."""
    sub: list[ComplianceResult] = []

    sub.append(
        ComplianceResult(
            compliant=clear_plain_language,
            section="Sec 6(3)",
            reason=(
                "clear and plain language used"
                if clear_plain_language
                else "consent request must be presented in clear and plain language"
            ),
            citation="DPDP Act 2023, Sec 6(3)",
        )
    )

    sub.append(
        ComplianceResult(
            compliant=eighth_schedule_option,
            section="Sec 6(3)",
            reason=(
                "Eighth Schedule language option given"
                if eighth_schedule_option
                else "must provide option to access request in English or Eighth Schedule language"
            ),
            citation="DPDP Act 2023, Sec 6(3)",
        )
    )

    sub.append(
        ComplianceResult(
            compliant=dpo_contact_provided,
            section="Sec 6(3)",
            reason=(
                "DPO or authorised person contact provided"
                if dpo_contact_provided
                else "must provide DPO or authorised person contact details for exercise of rights"
            ),
            citation="DPDP Act 2023, Sec 6(3)",
        )
    )

    all_pass = all(r.compliant for r in sub)
    failed = [r for r in sub if not r.compliant]
    return ComplianceResult(
        compliant=all_pass,
        section="Sec 6(3)",
        reason=(
            "consent request meets all Sec 6(3) requirements"
            if all_pass
            else f"{len(failed)} Sec 6(3) requirement(s) failed: "
            + "; ".join(r.reason for r in failed)
        ),
        citation="DPDP Act 2023, Sec 6(3)",
        sub_results=sub,
    )


def check_withdrawal_consequences(
    data_principal_informed_of_consequences: bool,
    pre_withdrawal_processing_treated_lawful: bool,
) -> ComplianceResult:
    """Sec 6(5) — consequences of withdrawal borne by Data Principal; pre-withdrawal processing lawful."""
    sub: list[ComplianceResult] = []

    sub.append(
        ComplianceResult(
            compliant=data_principal_informed_of_consequences,
            section="Sec 6(5)",
            reason=(
                "Data Principal informed consequences of withdrawal are borne by her"
                if data_principal_informed_of_consequences
                else "Data Fiduciary must inform Data Principal that consequences of withdrawal are borne by her"
            ),
            citation="DPDP Act 2023, Sec 6(5)",
        )
    )

    sub.append(
        ComplianceResult(
            compliant=pre_withdrawal_processing_treated_lawful,
            section="Sec 6(5)",
            reason=(
                "pre-withdrawal processing treated as lawful"
                if pre_withdrawal_processing_treated_lawful
                else "withdrawal shall not affect legality of processing based on consent before withdrawal"
            ),
            citation="DPDP Act 2023, Sec 6(5)",
        )
    )

    all_pass = all(r.compliant for r in sub)
    failed = [r for r in sub if not r.compliant]
    return ComplianceResult(
        compliant=all_pass,
        section="Sec 6(5)",
        reason=(
            "Sec 6(5) withdrawal consequences requirements met"
            if all_pass
            else f"{len(failed)} Sec 6(5) requirement(s) failed: "
            + "; ".join(r.reason for r in failed)
        ),
        citation="DPDP Act 2023, Sec 6(5)",
        sub_results=sub,
    )


def check_cessation_on_withdrawal(
    df_ceased_processing: bool,
    df_caused_processors_to_cease: bool,
    has_lawful_basis_for_continued_processing: bool,
) -> ComplianceResult:
    """Sec 6(6) — cease processing and cause processors to cease within reasonable time after withdrawal."""
    # ambiguity: "reasonable time" undefined — delegated to DPDP Rules 2025 or judicial interpretation

    if has_lawful_basis_for_continued_processing:
        return ComplianceResult(
            compliant=True,
            section="Sec 6(6)",
            reason="continued processing authorised under the Act, rules, or other law in force in India",
            citation="DPDP Act 2023, Sec 6(6)",
        )

    sub: list[ComplianceResult] = []

    sub.append(
        ComplianceResult(
            compliant=df_ceased_processing,
            section="Sec 6(6)(a)",
            reason=(
                "Data Fiduciary ceased processing within reasonable time"
                if df_ceased_processing
                else "Data Fiduciary must cease processing within a reasonable time after withdrawal"
            ),
            citation="DPDP Act 2023, Sec 6(6)(a)",
        )
    )

    sub.append(
        ComplianceResult(
            compliant=df_caused_processors_to_cease,
            section="Sec 6(6)(b)",
            reason=(
                "Data Fiduciary caused processors to cease"
                if df_caused_processors_to_cease
                else "Data Fiduciary must cause its Data Processors to cease processing after withdrawal"
            ),
            citation="DPDP Act 2023, Sec 6(6)(b)",
        )
    )

    all_pass = all(r.compliant for r in sub)
    failed = [r for r in sub if not r.compliant]
    return ComplianceResult(
        compliant=all_pass,
        section="Sec 6(6)",
        reason=(
            "processing ceased on withdrawal"
            if all_pass
            else f"{len(failed)} cessation requirement(s) failed: "
            + "; ".join(r.reason for r in failed)
        ),
        citation="DPDP Act 2023, Sec 6(6)",
        sub_results=sub,
    )


def check_consent_via_consent_manager(
    consent_via_consent_manager: bool,
    data_fiduciary_honours_consent_manager_consent: bool,
) -> ComplianceResult:
    """Sec 6(7) — Data Principal may give, manage, review or withdraw consent through a Consent Manager."""
    if not consent_via_consent_manager:
        return ComplianceResult(
            compliant=True,
            section="Sec 6(7)",
            reason="consent not routed through Consent Manager — Sec 6(7) not triggered",
            citation="DPDP Act 2023, Sec 6(7)",
        )

    return ComplianceResult(
        compliant=data_fiduciary_honours_consent_manager_consent,
        section="Sec 6(7)",
        reason=(
            "Data Fiduciary honours consent given via Consent Manager"
            if data_fiduciary_honours_consent_manager_consent
            else "Data Fiduciary must accept consent given, managed, reviewed or withdrawn via Consent Manager"
        ),
        citation="DPDP Act 2023, Sec 6(7)",
    )


def check_consent_manager_accountability(
    is_accountable_to_data_principal: bool,
    acts_on_behalf_of_data_principal: bool,
) -> ComplianceResult:
    """Sec 6(8) — Consent Manager accountable to Data Principal and acts on her behalf."""
    # delegated to DPDP Rules 2025 — manner and obligations prescribed
    sub: list[ComplianceResult] = []

    sub.append(
        ComplianceResult(
            compliant=is_accountable_to_data_principal,
            section="Sec 6(8)",
            reason=(
                "Consent Manager accountable to Data Principal"
                if is_accountable_to_data_principal
                else "Consent Manager must be accountable to the Data Principal"
            ),
            citation="DPDP Act 2023, Sec 6(8)",
        )
    )

    sub.append(
        ComplianceResult(
            compliant=acts_on_behalf_of_data_principal,
            section="Sec 6(8)",
            reason=(
                "Consent Manager acts on behalf of Data Principal"
                if acts_on_behalf_of_data_principal
                else "Consent Manager must act on behalf of the Data Principal"
            ),
            citation="DPDP Act 2023, Sec 6(8)",
        )
    )

    all_pass = all(r.compliant for r in sub)
    failed = [r for r in sub if not r.compliant]
    return ComplianceResult(
        compliant=all_pass,
        section="Sec 6(8)",
        reason=(
            "Consent Manager meets Sec 6(8) obligations"
            if all_pass
            else f"{len(failed)} Sec 6(8) requirement(s) failed: "
            + "; ".join(r.reason for r in failed)
        ),
        citation="DPDP Act 2023, Sec 6(8)",
        sub_results=sub,
    )


def check_consent_manager_registration(
    is_registered_with_board: bool,
) -> ComplianceResult:
    """Sec 6(9) — Consent Manager must be registered with the Board."""
    # delegated to DPDP Rules 2025 — manner and technical, operational, financial conditions prescribed
    return ComplianceResult(
        compliant=is_registered_with_board,
        section="Sec 6(9)",
        reason=(
            "Consent Manager registered with the Board"
            if is_registered_with_board
            else "every Consent Manager must be registered with the Board"
        ),
        citation="DPDP Act 2023, Sec 6(9)",
    )


def check_burden_of_proof(
    notice_given: bool,
    consent_obtained: bool,
    evidence_present: bool,
) -> ComplianceResult:
    """Sec 6(10) — burden of proof on Data Fiduciary to prove notice was given and consent was obtained."""
    sub: list[ComplianceResult] = []

    sub.append(
        ComplianceResult(
            compliant=notice_given,
            section="Sec 6(10)",
            reason=(
                "Data Fiduciary can prove notice was given to Data Principal"
                if notice_given
                else "Data Fiduciary must prove notice was given to Data Principal"
            ),
            citation="DPDP Act 2023, Sec 6(10)",
        )
    )

    sub.append(
        ComplianceResult(
            compliant=consent_obtained,
            section="Sec 6(10)",
            reason=(
                "Data Fiduciary can prove consent was obtained from Data Principal"
                if consent_obtained
                else "Data Fiduciary must prove consent was given by Data Principal"
            ),
            citation="DPDP Act 2023, Sec 6(10)",
        )
    )

    sub.append(
        ComplianceResult(
            compliant=evidence_present,
            section="Sec 6(10)",
            reason=(
                "burden of proof evidence available"
                if evidence_present
                else "Data Fiduciary must maintain evidence to discharge burden of proof in proceedings"
            ),
            citation="DPDP Act 2023, Sec 6(10)",
        )
    )

    all_pass = all(r.compliant for r in sub)
    failed = [r for r in sub if not r.compliant]
    return ComplianceResult(
        compliant=all_pass,
        section="Sec 6(10)",
        reason=(
            "burden of proof discharged"
            if all_pass
            else f"{len(failed)} burden-of-proof requirement(s) failed: "
            + "; ".join(r.reason for r in failed)
        ),
        citation="DPDP Act 2023, Sec 6(10)",
        sub_results=sub,
    )

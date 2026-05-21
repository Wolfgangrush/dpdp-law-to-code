"""Sec 5 — Notice.

Citation: DPDP Act 2023, Sec 5.
Last updated: 2026-05-23.

This module is not legal advice. It encodes a developer-friendly reading of
DPDP Act 2023 Sec 5 for compliance harness purposes. Consult qualified
counsel before relying on outputs for regulatory or contentious matters.
"""

from __future__ import annotations

from dpdp.exceptions import InvalidInputError
from dpdp.types import ComplianceResult, LegacyNoticeRecord, NoticeRecord


# Eighth Schedule languages (22): Assamese, Bengali, Bodo, Dogri, Gujarati,
# Hindi, Kannada, Kashmiri, Konkani, Maithili, Malayalam, Manipuri, Marathi,
# Nepali, Odia, Punjabi, Sanskrit, Santhali, Sindhi, Tamil, Telugu, Urdu.


# ═══════════════════════════════════════════════════════════════════════════
# Sec 5(1)(i) — notice describes personal data and purpose
# ═══════════════════════════════════════════════════════════════════════════

def check_notice_describes_data(notice: NoticeRecord) -> ComplianceResult:
    """Sec 5(1)(i) — notice describes the personal data to be processed and the purpose."""
    if not isinstance(notice, NoticeRecord):
        raise InvalidInputError("expected NoticeRecord", section="Sec 5(1)(i)")

    sub: list[ComplianceResult] = []

    sub.append(ComplianceResult(
        compliant=notice.describes_personal_data,
        section="Sec 5(1)(i)",
        reason=("describes personal data" if notice.describes_personal_data
                else "missing — the personal data proposed to be processed"),
        citation="DPDP Act 2023, Sec 5(1)(i)",
    ))

    sub.append(ComplianceResult(
        compliant=notice.describes_purpose,
        section="Sec 5(1)(i)",
        reason=("describes purpose" if notice.describes_purpose
                else "missing — the purpose for which personal data is proposed to be processed"),
        citation="DPDP Act 2023, Sec 5(1)(i)",
    ))

    all_pass = all(r.compliant for r in sub)
    failed = [r for r in sub if not r.compliant]
    return ComplianceResult(
        compliant=all_pass,
        section="Sec 5(1)(i)",
        reason=("notice describes personal data and purpose" if all_pass
                else f"{len(failed)} ingredient(s) missing: " + "; ".join(r.reason for r in failed)),
        citation="DPDP Act 2023, Sec 5(1)(i)",
        sub_results=sub,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 5(1)(ii) — notice describes manner of exercising rights
# ═══════════════════════════════════════════════════════════════════════════

def check_notice_rights_exercise(notice: NoticeRecord) -> ComplianceResult:
    """Sec 5(1)(ii) — notice describes manner of exercising rights under Sec 6(4) and Sec 13."""
    if not isinstance(notice, NoticeRecord):
        raise InvalidInputError("expected NoticeRecord", section="Sec 5(1)(ii)")

    return ComplianceResult(
        compliant=notice.describes_rights_exercise_method,
        section="Sec 5(1)(ii)",
        reason=("describes manner of exercising rights under Sec 6(4) and Sec 13"
                if notice.describes_rights_exercise_method
                else "missing — manner in which Data Principal may exercise rights under Sec 6(4) and Sec 13"),
        citation="DPDP Act 2023, Sec 5(1)(ii)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 5(1)(iii) — notice describes manner of complaint to Board
# ═══════════════════════════════════════════════════════════════════════════

def check_notice_board_complaint(notice: NoticeRecord) -> ComplianceResult:
    """Sec 5(1)(iii) — notice describes manner of complaint to Board."""
    if not isinstance(notice, NoticeRecord):
        raise InvalidInputError("expected NoticeRecord", section="Sec 5(1)(iii)")

    return ComplianceResult(
        compliant=notice.describes_complaint_method_to_board,
        section="Sec 5(1)(iii)",
        reason=("describes manner of complaint to Board"
                if notice.describes_complaint_method_to_board
                else "missing — manner in which Data Principal may make a complaint to the Board"),
        citation="DPDP Act 2023, Sec 5(1)(iii)",
    )
    # delegated to DPDP Rules 2025 — manner prescribed


# ═══════════════════════════════════════════════════════════════════════════
# Sec 5(1) — timing: notice before or at consent request
# ═══════════════════════════════════════════════════════════════════════════

def check_notice_timing(notice: NoticeRecord) -> ComplianceResult:
    """Sec 5(1) — notice must be given before or at the time of consent request."""
    if not isinstance(notice, NoticeRecord):
        raise InvalidInputError("expected NoticeRecord", section="Sec 5(1)")

    return ComplianceResult(
        compliant=notice.is_given_before_or_with_consent_request,
        section="Sec 5(1)",
        reason=("notice given before or at the time of consent request"
                if notice.is_given_before_or_with_consent_request
                else "notice must accompany or precede the request for consent"),
        citation="DPDP Act 2023, Sec 5(1)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 5(3) — language requirement
# ═══════════════════════════════════════════════════════════════════════════

def check_notice_language(notice: NoticeRecord) -> ComplianceResult:
    """Sec 5(3) — notice available in English or any Eighth Schedule language."""
    if not isinstance(notice, NoticeRecord):
        raise InvalidInputError("expected NoticeRecord", section="Sec 5(3)")

    return ComplianceResult(
        compliant=notice.available_in_english_or_eighth_schedule_language,
        section="Sec 5(3)",
        reason=("available in English or Eighth Schedule language"
                if notice.available_in_english_or_eighth_schedule_language
                else "notice must be available in English or any language in the Eighth Schedule to the Constitution"),
        citation="DPDP Act 2023, Sec 5(3)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Master Sec 5(1)-(3) aggregator
# ═══════════════════════════════════════════════════════════════════════════

def check_notice(notice: NoticeRecord) -> ComplianceResult:
    """Sec 5(1)-(3) — master notice validation aggregating ingredients, timing and language."""
    if not isinstance(notice, NoticeRecord):
        raise InvalidInputError("expected NoticeRecord", section="Sec 5")

    sub: list[ComplianceResult] = []
    sub.append(check_notice_describes_data(notice))
    sub.append(check_notice_rights_exercise(notice))
    sub.append(check_notice_board_complaint(notice))
    sub.append(check_notice_timing(notice))
    sub.append(check_notice_language(notice))

    all_pass = all(r.compliant for r in sub)
    failed = [r for r in sub if not r.compliant]
    return ComplianceResult(
        compliant=all_pass,
        section="Sec 5",
        reason=("all Sec 5 notice requirements satisfied" if all_pass
                else f"{len(failed)} of {len(sub)} requirement(s) failed: " + "; ".join(r.reason for r in failed)),
        citation="DPDP Act 2023, Sec 5",
        sub_results=sub,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 5(2) — legacy-data notice (data collected before Act commencement)
# ═══════════════════════════════════════════════════════════════════════════

def check_legacy_notice(legacy: LegacyNoticeRecord) -> ComplianceResult:
    """Sec 5(2) — legacy-data notice for personal data collected before Act commencement."""
    if not isinstance(legacy, LegacyNoticeRecord):
        raise InvalidInputError("expected LegacyNoticeRecord", section="Sec 5(2)")

    sub: list[ComplianceResult] = []

    # Sec 5(2)(i) — describes personal data processed + purpose
    sub.append(ComplianceResult(
        compliant=legacy.describes_personal_data,
        section="Sec 5(2)(i)",
        reason=("describes personal data processed" if legacy.describes_personal_data
                else "missing — the personal data that has been processed before Act commencement"),
        citation="DPDP Act 2023, Sec 5(2)(i)",
    ))
    sub.append(ComplianceResult(
        compliant=legacy.describes_purpose,
        section="Sec 5(2)(i)",
        reason=("describes purpose for which data has been processed" if legacy.describes_purpose
                else "missing — the purpose for which personal data has been processed"),
        citation="DPDP Act 2023, Sec 5(2)(i)",
    ))

    # Sec 5(2)(ii) — describes manner of exercising withdrawal + grievance rights
    sub.append(ComplianceResult(
        compliant=legacy.describes_rights_exercise_method,
        section="Sec 5(2)(ii)",
        reason=("describes manner of exercising rights under Sec 6(4) and Sec 13"
                if legacy.describes_rights_exercise_method
                else "missing — manner in which Data Principal may exercise rights under Sec 6(4) and Sec 13"),
        citation="DPDP Act 2023, Sec 5(2)(ii)",
    ))

    # Sec 5(2)(iii) — describes manner of complaint to Board
    sub.append(ComplianceResult(
        compliant=legacy.describes_complaint_method_to_board,
        section="Sec 5(2)(iii)",
        reason=("describes manner of complaint to Board"
                if legacy.describes_complaint_method_to_board
                else "missing — manner in which Data Principal may make a complaint to the Board"),
        citation="DPDP Act 2023, Sec 5(2)(iii)",
    ))
    # delegated to DPDP Rules 2025 — manner prescribed

    # Sec 5(2) — timing: must be given after Act commencement
    sub.append(ComplianceResult(
        compliant=legacy.given_after_act_commencement_date,
        section="Sec 5(2)",
        reason=("legacy notice given after Act commencement date"
                if legacy.given_after_act_commencement_date
                else "legacy notice must be given after the date of commencement of the Act"),
        citation="DPDP Act 2023, Sec 5(2)",
    ))

    # Sec 5(2) — timing: must be given within reasonable time
    sub.append(ComplianceResult(
        compliant=legacy.given_within_reasonable_time,
        section="Sec 5(2)",
        reason=("legacy notice given within reasonable time"
                if legacy.given_within_reasonable_time
                else "legacy notice not given as soon as reasonably practicable"),
        citation="DPDP Act 2023, Sec 5(2)",
    ))
    # ambiguity: "as soon as reasonably practicable" undefined; v0.1 uses bool heuristic

    # Sec 5(3) — language applies to both 5(1) and 5(2) notices
    sub.append(ComplianceResult(
        compliant=legacy.available_in_english_or_eighth_schedule_language,
        section="Sec 5(3)",
        reason=("available in English or Eighth Schedule language"
                if legacy.available_in_english_or_eighth_schedule_language
                else "legacy notice must be available in English or any Eighth Schedule language"),
        citation="DPDP Act 2023, Sec 5(3)",
    ))

    all_pass = all(r.compliant for r in sub)
    failed = [r for r in sub if not r.compliant]
    return ComplianceResult(
        compliant=all_pass,
        section="Sec 5(2)",
        reason=("all Sec 5(2) legacy notice requirements satisfied" if all_pass
                else f"{len(failed)} of {len(sub)} legacy-notice requirement(s) failed: " + "; ".join(r.reason for r in failed)),
        citation="DPDP Act 2023, Sec 5(2)",
        sub_results=sub,
    )

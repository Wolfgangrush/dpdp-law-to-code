"""Sec 5 notice test suite — covers all obligations in Sec 5(1)-(3)."""

from __future__ import annotations

import pytest

from dpdp.exceptions import InvalidInputError
from dpdp.notice import (
    LegacyNoticeRecord,
    check_legacy_notice,
    check_notice,
    check_notice_board_complaint,
    check_notice_describes_data,
    check_notice_language,
    check_notice_rights_exercise,
    check_notice_timing,
)
from dpdp.types import NoticeRecord


def _good_notice() -> NoticeRecord:
    return NoticeRecord(
        describes_personal_data=True,
        describes_purpose=True,
        describes_rights_exercise_method=True,
        describes_complaint_method_to_board=True,
        available_in_english_or_eighth_schedule_language=True,
        is_given_before_or_with_consent_request=True,
    )


def _good_legacy() -> LegacyNoticeRecord:
    return LegacyNoticeRecord(
        describes_personal_data=True,
        describes_purpose=True,
        describes_rights_exercise_method=True,
        describes_complaint_method_to_board=True,
        available_in_english_or_eighth_schedule_language=True,
        given_after_act_commencement_date=True,
        given_within_reasonable_time=True,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 5(1)(i) — notice describes personal data and purpose
# ═══════════════════════════════════════════════════════════════════════════


def test_sec5_1_i_pass():
    r = check_notice_describes_data(_good_notice())
    assert r.compliant is True
    assert len(r.sub_results) == 2
    assert all(s.compliant for s in r.sub_results)


def test_sec5_1_i_fail_missing_data():
    n = NoticeRecord(
        describes_personal_data=False,
        describes_purpose=True,
        describes_rights_exercise_method=True,
        describes_complaint_method_to_board=True,
        available_in_english_or_eighth_schedule_language=True,
        is_given_before_or_with_consent_request=True,
    )
    r = check_notice_describes_data(n)
    assert r.compliant is False
    assert r.sub_results[0].compliant is False
    assert "personal data" in r.sub_results[0].reason


def test_sec5_1_i_fail_missing_purpose():
    n = NoticeRecord(
        describes_personal_data=True,
        describes_purpose=False,
        describes_rights_exercise_method=True,
        describes_complaint_method_to_board=True,
        available_in_english_or_eighth_schedule_language=True,
        is_given_before_or_with_consent_request=True,
    )
    r = check_notice_describes_data(n)
    assert r.compliant is False
    assert r.sub_results[1].compliant is False
    assert "purpose" in r.sub_results[1].reason


def test_sec5_1_i_fail_both_missing():
    n = NoticeRecord(
        describes_personal_data=False,
        describes_purpose=False,
        describes_rights_exercise_method=True,
        describes_complaint_method_to_board=True,
        available_in_english_or_eighth_schedule_language=True,
        is_given_before_or_with_consent_request=True,
    )
    r = check_notice_describes_data(n)
    assert r.compliant is False
    assert len(r.sub_results) == 2
    assert all(not s.compliant for s in r.sub_results)


def test_sec5_1_i_invalid_input():
    with pytest.raises(InvalidInputError) as exc:
        check_notice_describes_data("not a NoticeRecord")  # type: ignore[arg-type]
    assert "Sec 5(1)(i)" in str(exc.value)


# ═══════════════════════════════════════════════════════════════════════════
# Sec 5(1)(ii) — notice describes manner of exercising rights
# ═══════════════════════════════════════════════════════════════════════════


def test_sec5_1_ii_pass():
    r = check_notice_rights_exercise(_good_notice())
    assert r.compliant is True
    assert "Sec 6(4)" in r.reason


def test_sec5_1_ii_fail():
    n = NoticeRecord(
        describes_personal_data=True,
        describes_purpose=True,
        describes_rights_exercise_method=False,
        describes_complaint_method_to_board=True,
        available_in_english_or_eighth_schedule_language=True,
        is_given_before_or_with_consent_request=True,
    )
    r = check_notice_rights_exercise(n)
    assert r.compliant is False
    assert "Sec 6(4)" in r.reason


def test_sec5_1_ii_invalid_input():
    with pytest.raises(InvalidInputError) as exc:
        check_notice_rights_exercise(None)  # type: ignore[arg-type]
    assert "Sec 5(1)(ii)" in str(exc.value)


# ═══════════════════════════════════════════════════════════════════════════
# Sec 5(1)(iii) — notice describes manner of complaint to Board
# ═══════════════════════════════════════════════════════════════════════════


def test_sec5_1_iii_pass():
    r = check_notice_board_complaint(_good_notice())
    assert r.compliant is True
    assert "Board" in r.reason


def test_sec5_1_iii_fail():
    n = NoticeRecord(
        describes_personal_data=True,
        describes_purpose=True,
        describes_rights_exercise_method=True,
        describes_complaint_method_to_board=False,
        available_in_english_or_eighth_schedule_language=True,
        is_given_before_or_with_consent_request=True,
    )
    r = check_notice_board_complaint(n)
    assert r.compliant is False
    assert "Board" in r.reason


def test_sec5_1_iii_invalid_input():
    with pytest.raises(InvalidInputError) as exc:
        check_notice_board_complaint(42)  # type: ignore[arg-type]
    assert "Sec 5(1)(iii)" in str(exc.value)


# ═══════════════════════════════════════════════════════════════════════════
# Sec 5(1) — timing: notice before or at consent request
# ═══════════════════════════════════════════════════════════════════════════


def test_sec5_1_timing_pass():
    r = check_notice_timing(_good_notice())
    assert r.compliant is True


def test_sec5_1_timing_fail():
    n = NoticeRecord(
        describes_personal_data=True,
        describes_purpose=True,
        describes_rights_exercise_method=True,
        describes_complaint_method_to_board=True,
        available_in_english_or_eighth_schedule_language=True,
        is_given_before_or_with_consent_request=False,
    )
    r = check_notice_timing(n)
    assert r.compliant is False
    assert (
        "before" in r.reason.lower()
        or "accompany" in r.reason.lower()
        or "precede" in r.reason.lower()
    )


def test_sec5_1_timing_invalid_input():
    with pytest.raises(InvalidInputError) as exc:
        check_notice_timing([])  # type: ignore[arg-type]
    assert "Sec 5(1)" in str(exc.value)


# ═══════════════════════════════════════════════════════════════════════════
# Sec 5(3) — language requirement
# ═══════════════════════════════════════════════════════════════════════════


def test_sec5_3_pass():
    r = check_notice_language(_good_notice())
    assert r.compliant is True


def test_sec5_3_fail():
    n = NoticeRecord(
        describes_personal_data=True,
        describes_purpose=True,
        describes_rights_exercise_method=True,
        describes_complaint_method_to_board=True,
        available_in_english_or_eighth_schedule_language=False,
        is_given_before_or_with_consent_request=True,
    )
    r = check_notice_language(n)
    assert r.compliant is False
    assert "Eighth Schedule" in r.reason


def test_sec5_3_invalid_input():
    with pytest.raises(InvalidInputError) as exc:
        check_notice_language({})  # type: ignore[arg-type]
    assert "Sec 5(3)" in str(exc.value)


# ═══════════════════════════════════════════════════════════════════════════
# Master check_notice — Sec 5(1)-(3) aggregator
# ═══════════════════════════════════════════════════════════════════════════


def test_check_notice_all_pass():
    r = check_notice(_good_notice())
    assert r.compliant is True
    assert r.section == "Sec 5"
    assert len(r.sub_results) == 5


def test_check_notice_single_field_fails():
    n = NoticeRecord(
        describes_personal_data=True,
        describes_purpose=True,
        describes_rights_exercise_method=True,
        describes_complaint_method_to_board=False,  # single failure
        available_in_english_or_eighth_schedule_language=True,
        is_given_before_or_with_consent_request=True,
    )
    r = check_notice(n)
    assert r.compliant is False
    assert "1 of 5" in r.reason


def test_check_notice_all_fail():
    n = NoticeRecord(
        describes_personal_data=False,
        describes_purpose=False,
        describes_rights_exercise_method=False,
        describes_complaint_method_to_board=False,
        available_in_english_or_eighth_schedule_language=False,
        is_given_before_or_with_consent_request=False,
    )
    r = check_notice(n)
    assert r.compliant is False
    assert "5 of 5" in r.reason


def test_check_notice_invalid_input():
    with pytest.raises(InvalidInputError) as exc:
        check_notice("bad")  # type: ignore[arg-type]
    assert "Sec 5" in str(exc.value)


# ═══════════════════════════════════════════════════════════════════════════
# Sec 5(2) — legacy-data notice
# ═══════════════════════════════════════════════════════════════════════════


def test_sec5_2_pass():
    r = check_legacy_notice(_good_legacy())
    assert r.compliant is True
    assert r.section == "Sec 5(2)"
    assert (
        len(r.sub_results) == 7
    )  # data, purpose, rights, complaint, commencement-timing, reasonable-time, language


def test_sec5_2_fail_missing_ingredients():
    leg = LegacyNoticeRecord(
        describes_personal_data=False,
        describes_purpose=False,
        describes_rights_exercise_method=False,
        describes_complaint_method_to_board=False,
        available_in_english_or_eighth_schedule_language=True,
        given_after_act_commencement_date=True,
        given_within_reasonable_time=True,
    )
    r = check_legacy_notice(leg)
    assert r.compliant is False
    # data, purpose, rights, complaint = 4 failing sub-results
    assert any("5(2)(i)" in s.section for s in r.sub_results if not s.compliant)
    assert any("5(2)(ii)" in s.section for s in r.sub_results if not s.compliant)
    assert any("5(2)(iii)" in s.section for s in r.sub_results if not s.compliant)


def test_sec5_2_fail_not_after_commencement():
    leg = LegacyNoticeRecord(
        describes_personal_data=True,
        describes_purpose=True,
        describes_rights_exercise_method=True,
        describes_complaint_method_to_board=True,
        available_in_english_or_eighth_schedule_language=True,
        given_after_act_commencement_date=False,
        given_within_reasonable_time=True,
    )
    r = check_legacy_notice(leg)
    assert r.compliant is False
    assert any(
        "commencement" in s.reason.lower() for s in r.sub_results if not s.compliant
    )


def test_sec5_2_fail_not_reasonable_time():
    leg = LegacyNoticeRecord(
        describes_personal_data=True,
        describes_purpose=True,
        describes_rights_exercise_method=True,
        describes_complaint_method_to_board=True,
        available_in_english_or_eighth_schedule_language=True,
        given_after_act_commencement_date=True,
        given_within_reasonable_time=False,
    )
    r = check_legacy_notice(leg)
    assert r.compliant is False
    assert any(
        "reasonably practicable" in s.reason.lower()
        for s in r.sub_results
        if not s.compliant
    )


def test_sec5_2_fail_language():
    leg = LegacyNoticeRecord(
        describes_personal_data=True,
        describes_purpose=True,
        describes_rights_exercise_method=True,
        describes_complaint_method_to_board=True,
        available_in_english_or_eighth_schedule_language=False,
        given_after_act_commencement_date=True,
        given_within_reasonable_time=True,
    )
    r = check_legacy_notice(leg)
    assert r.compliant is False
    assert any("Eighth Schedule" in s.reason for s in r.sub_results if not s.compliant)


def test_sec5_2_invalid_input():
    with pytest.raises(InvalidInputError) as exc:
        check_legacy_notice(_good_notice())  # type: ignore[arg-type]
    assert "Sec 5(2)" in str(exc.value)

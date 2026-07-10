"""Sec 6 consent test suite — covers all obligations in Sec 6(1)-(10)."""

from __future__ import annotations
import pytest
from dpdp.consent import (
    check_consent,
    check_withdrawal_ease,
    check_infringing_consent,
    check_consent_request_presentation,
    check_withdrawal_consequences,
    check_cessation_on_withdrawal,
    check_consent_via_consent_manager,
    check_consent_manager_accountability,
    check_consent_manager_registration,
    check_burden_of_proof,
)
from dpdp.exceptions import InvalidInputError
from dpdp.types import ConsentRecord


def _good() -> ConsentRecord:
    return ConsentRecord(
        is_free=True,
        is_specific=True,
        is_informed=True,
        is_unconditional=True,
        is_unambiguous=True,
        has_clear_affirmative_action=True,
        is_limited_to_specified_purpose=True,
        is_withdrawable_easily=True,
        is_pre_checked=False,
        is_bundled_with_unrelated_terms=False,
        has_infringing_provision=False,
        request_in_clear_plain_language=True,
        has_eighth_schedule_language_option=True,
        dpo_contact_provided=True,
    )


# -- existing tests (preserved) --------------------------------------------------


def test_all_pass():
    assert check_consent(_good()).compliant is True


def test_pre_checked_box_fails():
    assert not check_consent(
        ConsentRecord(**{**_good().__dict__, "is_pre_checked": True})
    ).compliant


def test_bundled_consent_fails():
    assert not check_consent(
        ConsentRecord(**{**_good().__dict__, "is_bundled_with_unrelated_terms": True})
    ).compliant


def test_not_free_fails():
    assert not check_consent(
        ConsentRecord(**{**_good().__dict__, "is_free": False})
    ).compliant


def test_not_specific_fails():
    assert not check_consent(
        ConsentRecord(**{**_good().__dict__, "is_specific": False})
    ).compliant


def test_not_informed_fails():
    assert not check_consent(
        ConsentRecord(**{**_good().__dict__, "is_informed": False})
    ).compliant


def test_not_unconditional_fails():
    assert not check_consent(
        ConsentRecord(**{**_good().__dict__, "is_unconditional": False})
    ).compliant


def test_not_unambiguous_fails():
    assert not check_consent(
        ConsentRecord(**{**_good().__dict__, "is_unambiguous": False})
    ).compliant


def test_withdrawal_harder_fails():
    assert not check_consent(
        ConsentRecord(**{**_good().__dict__, "is_withdrawable_easily": False})
    ).compliant


def test_standalone_withdrawal_check():
    assert check_withdrawal_ease(_good()).compliant is True
    assert not check_withdrawal_ease(
        ConsentRecord(**{**_good().__dict__, "is_withdrawable_easily": False})
    ).compliant


def test_invalid_input_raises():
    with pytest.raises(InvalidInputError):
        check_consent("not a ConsentRecord")


# -- Sec 6(2) infringing consent --------------------------------------------------


def test_sec6_2_pass():
    """No infringing provision — consent is valid."""
    r = check_consent(_good())
    sec6_2 = [s for s in r.sub_results if s.section == "Sec 6(2)"]
    assert all(s.compliant for s in sec6_2)

    standalone = check_infringing_consent(False)
    assert standalone.compliant is True


def test_sec6_2_fail():
    """Infringing provision present — consent invalid to that extent."""
    bad = ConsentRecord(**{**_good().__dict__, "has_infringing_provision": True})
    r = check_consent(bad)
    sec6_2 = [s for s in r.sub_results if s.section == "Sec 6(2)"]
    assert not all(s.compliant for s in sec6_2)

    standalone = check_infringing_consent(True)
    assert standalone.compliant is False


# -- Sec 6(3) consent request presentation ----------------------------------------


def test_sec6_3_pass():
    """All three language/DPO requirements met."""
    r = check_consent(_good())
    sec6_3 = [s for s in r.sub_results if s.section == "Sec 6(3)"]
    assert len(sec6_3) == 3
    assert all(s.compliant for s in sec6_3)

    standalone = check_consent_request_presentation(True, True, True)
    assert standalone.compliant is True


def test_sec6_3_fail():
    """Missing clear language, Eighth Schedule option, and DPO contact."""
    bad = ConsentRecord(
        **{
            **_good().__dict__,
            "request_in_clear_plain_language": False,
            "has_eighth_schedule_language_option": False,
            "dpo_contact_provided": False,
        }
    )
    r = check_consent(bad)
    sec6_3 = [s for s in r.sub_results if s.section == "Sec 6(3)"]
    assert len(sec6_3) == 3
    assert not any(s.compliant for s in sec6_3)

    standalone = check_consent_request_presentation(False, False, False)
    assert standalone.compliant is False


def test_sec6_3_partial_fail_clear_language():
    """Only clear/plain language missing."""
    standalone = check_consent_request_presentation(False, True, True)
    assert standalone.compliant is False
    subs = standalone.sub_results
    assert not subs[0].compliant  # clear language
    assert subs[1].compliant  # Eighth Schedule
    assert subs[2].compliant  # DPO contact


# -- Sec 6(5) withdrawal consequences ---------------------------------------------


def test_sec6_5_pass():
    """Data Principal informed of consequences; pre-withdrawal processing treated as lawful."""
    r = check_withdrawal_consequences(True, True)
    assert r.compliant is True
    assert all(s.compliant for s in r.sub_results)


def test_sec6_5_fail():
    """Neither obligation met — consequences not communicated; pre-withdrawal processing invalidated."""
    r = check_withdrawal_consequences(False, False)
    assert r.compliant is False
    assert not any(s.compliant for s in r.sub_results)


def test_sec6_5_partial_fail_not_informed():
    """Data Principal not informed that consequences are borne by her."""
    r = check_withdrawal_consequences(False, True)
    assert r.compliant is False
    assert not r.sub_results[0].compliant
    assert r.sub_results[1].compliant


# -- Sec 6(6) cessation on withdrawal ---------------------------------------------


def test_sec6_6_pass():
    """Data Fiduciary ceased processing and caused processors to cease after withdrawal."""
    r = check_cessation_on_withdrawal(True, True, False)
    assert r.compliant is True
    assert all(s.compliant for s in r.sub_results)


def test_sec6_6_pass_lawful_basis():
    """Continued processing authorised under law — cessation not required."""
    r = check_cessation_on_withdrawal(False, False, True)
    assert r.compliant is True


def test_sec6_6_fail():
    """Neither DF nor processors ceased processing after withdrawal, and no lawful basis."""
    r = check_cessation_on_withdrawal(False, False, False)
    assert r.compliant is False
    assert not any(s.compliant for s in r.sub_results)


def test_sec6_6_partial_fail_df_only():
    """DF ceased but failed to cause processors to cease."""
    r = check_cessation_on_withdrawal(True, False, False)
    assert r.compliant is False
    assert r.sub_results[0].compliant
    assert not r.sub_results[1].compliant


# -- Sec 6(7) consent via Consent Manager -----------------------------------------


def test_sec6_7_pass():
    """Consent not via Consent Manager — Sec 6(7) not triggered."""
    r = check_consent_via_consent_manager(False, False)
    assert r.compliant is True


def test_sec6_7_pass_via_manager():
    """Consent via Consent Manager and Data Fiduciary honours it."""
    r = check_consent_via_consent_manager(True, True)
    assert r.compliant is True


def test_sec6_7_fail():
    """Consent via Consent Manager but Data Fiduciary refuses to honour it."""
    r = check_consent_via_consent_manager(True, False)
    assert r.compliant is False


# -- Sec 6(8) Consent Manager accountability --------------------------------------


def test_sec6_8_pass():
    """Consent Manager accountable to DP and acts on her behalf."""
    r = check_consent_manager_accountability(True, True)
    assert r.compliant is True
    assert all(s.compliant for s in r.sub_results)


def test_sec6_8_fail():
    """Consent Manager neither accountable nor acting on behalf of DP."""
    r = check_consent_manager_accountability(False, False)
    assert r.compliant is False
    assert not any(s.compliant for s in r.sub_results)


def test_sec6_8_partial_fail_not_accountable():
    """Consent Manager acts on behalf but not accountable to DP."""
    r = check_consent_manager_accountability(False, True)
    assert r.compliant is False
    assert not r.sub_results[0].compliant
    assert r.sub_results[1].compliant


# -- Sec 6(9) Consent Manager registration ----------------------------------------


def test_sec6_9_pass():
    """Consent Manager registered with the Board."""
    r = check_consent_manager_registration(True)
    assert r.compliant is True


def test_sec6_9_fail():
    """Consent Manager not registered with the Board."""
    r = check_consent_manager_registration(False)
    assert r.compliant is False


# -- Sec 6(10) burden of proof ----------------------------------------------------


def test_sec6_10_pass():
    """All three proof elements met — burden discharged."""
    r = check_burden_of_proof(True, True, True)
    assert r.compliant is True
    assert all(s.compliant for s in r.sub_results)


def test_sec6_10_fail():
    """No proof elements met — burden not discharged."""
    r = check_burden_of_proof(False, False, False)
    assert r.compliant is False
    assert not any(s.compliant for s in r.sub_results)


def test_sec6_10_partial_fail_no_notice():
    """Notice not proved; consent and evidence present."""
    r = check_burden_of_proof(False, True, True)
    assert r.compliant is False
    assert not r.sub_results[0].compliant
    assert r.sub_results[1].compliant
    assert r.sub_results[2].compliant

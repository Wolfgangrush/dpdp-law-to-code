"""Sec 9 children test suite — covers all obligations in Sec 9(1)-(5)."""

from __future__ import annotations

import pytest

from dpdp.children import (
    check_child_processing,
    check_parental_consent,
    check_disability_proviso,
    check_detrimental_effect,
    check_tracking_prohibition,
    check_targeted_ads_prohibition,
    check_class_exemption,
    check_age_threshold_exemption,
)
from dpdp.exceptions import InvalidInputError
from dpdp.types import ChildRecord


# ─── helpers ───────────────────────────────────────────────────────────────


def _compliant_child() -> ChildRecord:
    """A fully compliant child processing scenario."""
    return ChildRecord(
        data_principal_age=14,
        has_verifiable_parental_consent=True,
        is_tracking_behavior=False,
        is_targeted_advertising=False,
        is_likely_to_cause_detrimental_effect=False,
        is_class_exempted_by_notification=False,
    )


def _non_compliant_child() -> ChildRecord:
    """A fully non-compliant child processing scenario — all flags fail."""
    return ChildRecord(
        data_principal_age=10,
        has_verifiable_parental_consent=False,
        is_tracking_behavior=True,
        is_targeted_advertising=True,
        is_likely_to_cause_detrimental_effect=True,
        is_class_exempted_by_notification=False,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 9(1) — verifiable parental consent
# ═══════════════════════════════════════════════════════════════════════════


def test_sec9_1_pass_parental_consent_obtained():
    """Edutech platform obtains verifiable parental consent for 14yo."""
    record = ChildRecord(
        data_principal_age=14,
        has_verifiable_parental_consent=True,
        is_tracking_behavior=False,
        is_targeted_advertising=False,
        is_likely_to_cause_detrimental_effect=False,
    )
    r = check_parental_consent(record)
    assert r.compliant is True
    assert "verifiable parental consent obtained" in r.reason


def test_sec9_1_fail_no_parental_consent():
    """Edutech platform processing 14yo data without parental consent."""
    record = ChildRecord(
        data_principal_age=14,
        has_verifiable_parental_consent=False,
        is_tracking_behavior=False,
        is_targeted_advertising=False,
        is_likely_to_cause_detrimental_effect=False,
    )
    r = check_parental_consent(record)
    assert r.compliant is False
    assert "Sec 9(1) requires" in r.reason


def test_sec9_1_master_fails_when_consent_missing():
    """Master aggregates: parental consent missing fails overall check."""
    record = _non_compliant_child()
    r = check_child_processing(record)
    assert r.compliant is False
    sub_sections = {sr.section for sr in r.sub_results}
    assert "Sec 9(1)" in sub_sections


# ═══════════════════════════════════════════════════════════════════════════
# Sec 9(1) proviso — disability + lawful guardian
# ═══════════════════════════════════════════════════════════════════════════


def test_sec9_1_proviso_not_triggered_by_default():
    """Proviso not triggered when Data Principal is not a person with disability."""
    record = _compliant_child()
    r = check_disability_proviso(record)
    assert r.compliant is True
    assert "not triggered" in r.reason


def test_sec9_1_proviso_not_triggered_no_lawful_guardian():
    """Person with disability but no lawful guardian — proviso not triggered."""
    record = _compliant_child()
    r = check_disability_proviso(
        record, is_person_with_disability=True, has_lawful_guardian=False
    )
    assert r.compliant is True
    assert "not triggered" in r.reason


def test_sec9_1_proviso_pass_with_guardian_consent():
    """Person with disability + lawful guardian + verifiable consent obtained."""
    record = ChildRecord(
        data_principal_age=16,
        has_verifiable_parental_consent=True,
        is_tracking_behavior=False,
        is_targeted_advertising=False,
        is_likely_to_cause_detrimental_effect=False,
    )
    r = check_disability_proviso(
        record, is_person_with_disability=True, has_lawful_guardian=True
    )
    assert r.compliant is True
    assert "verifiable lawful guardian consent obtained" in r.reason


def test_sec9_1_proviso_fail_no_guardian_consent():
    """Person with disability + lawful guardian but no verifiable consent."""
    record = ChildRecord(
        data_principal_age=16,
        has_verifiable_parental_consent=False,
        is_tracking_behavior=False,
        is_targeted_advertising=False,
        is_likely_to_cause_detrimental_effect=False,
    )
    r = check_disability_proviso(
        record, is_person_with_disability=True, has_lawful_guardian=True
    )
    assert r.compliant is False
    assert "lawful guardian" in r.reason


# ═══════════════════════════════════════════════════════════════════════════
# Sec 9(2) — detrimental effect on child's well-being
# ═══════════════════════════════════════════════════════════════════════════


def test_sec9_2_pass_no_detrimental_effect():
    """Processing does not harm child's well-being."""
    record = _compliant_child()
    r = check_detrimental_effect(record)
    assert r.compliant is True
    assert "not detrimental" in r.reason


def test_sec9_2_fail_detrimental_effect():
    """Processing likely to cause detrimental effect on child's well-being."""
    record = ChildRecord(
        data_principal_age=12,
        has_verifiable_parental_consent=True,
        is_tracking_behavior=False,
        is_targeted_advertising=False,
        is_likely_to_cause_detrimental_effect=True,
    )
    r = check_detrimental_effect(record)
    assert r.compliant is False
    assert "detrimental effect" in r.reason


def test_sec9_2_master_includes_detrimental_check():
    """Master check includes Sec 9(2) in sub_results even when other checks pass."""
    record = ChildRecord(
        data_principal_age=14,
        has_verifiable_parental_consent=True,
        is_tracking_behavior=False,
        is_targeted_advertising=False,
        is_likely_to_cause_detrimental_effect=False,
    )
    r = check_child_processing(record)
    sub_sections = {sr.section for sr in r.sub_results}
    assert "Sec 9(2)" in sub_sections


# ═══════════════════════════════════════════════════════════════════════════
# Sec 9(3) — tracking prohibition
# ═══════════════════════════════════════════════════════════════════════════


def test_sec9_3_tracking_pass():
    """No behavioural tracking of child."""
    record = _compliant_child()
    r = check_tracking_prohibition(record)
    assert r.compliant is True
    assert "no tracking" in r.reason.lower()


def test_sec9_3_tracking_fail():
    """Gaming app tracks behavioural patterns of a 12yo."""
    record = ChildRecord(
        data_principal_age=12,
        has_verifiable_parental_consent=True,
        is_tracking_behavior=True,
        is_targeted_advertising=False,
        is_likely_to_cause_detrimental_effect=False,
    )
    r = check_tracking_prohibition(record)
    assert r.compliant is False
    assert "tracking" in r.reason


# ═══════════════════════════════════════════════════════════════════════════
# Sec 9(3) — targeted advertising prohibition
# ═══════════════════════════════════════════════════════════════════════════


def test_sec9_3_ads_pass():
    """No targeted advertising directed at child."""
    record = _compliant_child()
    r = check_targeted_ads_prohibition(record)
    assert r.compliant is True
    assert "no targeted advertising" in r.reason.lower()


def test_sec9_3_ads_fail():
    """Game shows behavioural ads to a 12yo."""
    record = ChildRecord(
        data_principal_age=12,
        has_verifiable_parental_consent=True,
        is_tracking_behavior=False,
        is_targeted_advertising=True,
        is_likely_to_cause_detrimental_effect=False,
    )
    r = check_targeted_ads_prohibition(record)
    assert r.compliant is False
    assert "targeted advertising" in r.reason


def test_sec9_3_both_tracking_and_ads_fail():
    """12yo subjected to both tracking and targeted ads — both checks fail."""
    record = ChildRecord(
        data_principal_age=12,
        has_verifiable_parental_consent=True,
        is_tracking_behavior=True,
        is_targeted_advertising=True,
        is_likely_to_cause_detrimental_effect=False,
    )
    r = check_child_processing(record)
    assert r.compliant is False
    sub_sections = {sr.section for sr in r.sub_results}
    assert "Sec 9(3)" in sub_sections


# ═══════════════════════════════════════════════════════════════════════════
# Sec 9(4) — class exemption
# ═══════════════════════════════════════════════════════════════════════════


def test_sec9_4_exemption_applies():
    """Data Fiduciary falls within Central Govt exemption notification."""
    record = ChildRecord(
        data_principal_age=14,
        has_verifiable_parental_consent=False,
        is_tracking_behavior=True,
        is_targeted_advertising=True,
        is_likely_to_cause_detrimental_effect=False,
        is_class_exempted_by_notification=True,
    )
    r = check_class_exemption(record)
    assert r.compliant is True
    assert "exemption notification" in r.reason


def test_sec9_4_exemption_not_applicable():
    """No exemption notification — normal Sec 9 rules apply."""
    record = _compliant_child()
    r = check_class_exemption(record)
    assert r.compliant is True
    assert "no class exemption" in r.reason


def test_sec9_4_master_short_circuits():
    """Master returns compliant=True immediately when class-exempted, regardless of other violations."""
    record = ChildRecord(
        data_principal_age=10,
        has_verifiable_parental_consent=False,
        is_tracking_behavior=True,
        is_targeted_advertising=True,
        is_likely_to_cause_detrimental_effect=True,
        is_class_exempted_by_notification=True,
    )
    r = check_child_processing(record)
    assert r.compliant is True
    assert "Sec 9(4)" in r.section


# ═══════════════════════════════════════════════════════════════════════════
# Sec 9(5) — lowered age threshold notification
# ═══════════════════════════════════════════════════════════════════════════


def test_sec9_5_no_notification_default():
    """No lowered-age notification — default 18-year threshold stands."""
    record = _compliant_child()
    r = check_age_threshold_exemption(record)
    assert r.compliant is True
    assert "default 18-year threshold" in r.reason


def test_sec9_5_notification_applies():
    """Data Fiduciary benefits from Central Govt lowered-age notification."""
    record = _compliant_child()
    r = check_age_threshold_exemption(record, age_lowered_by_notification=True)
    assert r.compliant is True
    assert "lowered-age notification" in r.reason


def test_sec9_5_master_exempts_tracking_and_ads():
    """When age_lowered_by_notification=True, master skips 9(3) tracking/ads checks."""
    record = ChildRecord(
        data_principal_age=15,
        has_verifiable_parental_consent=True,
        is_tracking_behavior=True,
        is_targeted_advertising=True,
        is_likely_to_cause_detrimental_effect=False,
    )
    r = check_child_processing(record, age_lowered_by_notification=True)
    # 9(1) passes, 9(2) passes, 9(5) exemption replaces 9(3) checks
    assert r.compliant is True
    sub_sections = {sr.section for sr in r.sub_results}
    assert "Sec 9(5)" in sub_sections
    # tracking/ads checks should not be in sub_results when exempted
    tracking_checks = [sr for sr in r.sub_results if sr.section == "Sec 9(3)"]
    assert len(tracking_checks) == 0


# ═══════════════════════════════════════════════════════════════════════════
# Master — age threshold (adult Data Principals)
# ═══════════════════════════════════════════════════════════════════════════


def test_master_adult_not_applicable():
    """18yo — Sec 9 does not apply, master returns compliant=True."""
    record = ChildRecord(
        data_principal_age=18,
        has_verifiable_parental_consent=False,
        is_tracking_behavior=True,
        is_targeted_advertising=True,
        is_likely_to_cause_detrimental_effect=True,
    )
    r = check_child_processing(record)
    assert r.compliant is True
    assert "not a child" in r.reason


def test_master_adult_25_not_applicable():
    """25yo adult — Sec 9 not applicable regardless of other flags."""
    record = ChildRecord(
        data_principal_age=25,
        has_verifiable_parental_consent=False,
        is_tracking_behavior=True,
        is_targeted_advertising=True,
        is_likely_to_cause_detrimental_effect=True,
    )
    r = check_child_processing(record)
    assert r.compliant is True
    assert ">= 18" in r.reason


def test_master_17yo_sec9_applies():
    """17yo signs up for adult finance app — Sec 9 applies, parental consent required."""
    record = ChildRecord(
        data_principal_age=17,
        has_verifiable_parental_consent=False,
        is_tracking_behavior=False,
        is_targeted_advertising=False,
        is_likely_to_cause_detrimental_effect=False,
    )
    r = check_child_processing(record)
    assert r.compliant is False
    sub_sections = {sr.section for sr in r.sub_results}
    assert "Sec 9(1)" in sub_sections


# ═══════════════════════════════════════════════════════════════════════════
# Master — fully compliant child processing
# ═══════════════════════════════════════════════════════════════════════════


def test_master_all_pass():
    """All Sec 9 obligations satisfied — fully compliant child processing."""
    record = _compliant_child()
    r = check_child_processing(record)
    assert r.compliant is True
    assert "all sec 9" in r.reason.lower()
    assert (
        len(r.sub_results) >= 4
    )  # consent, disability proviso, detrimental, tracking, ads


def test_master_all_fail():
    """Every Sec 9 obligation violated — comprehensive failure."""
    record = _non_compliant_child()
    r = check_child_processing(record)
    assert r.compliant is False
    failed = [sr for sr in r.sub_results if not sr.compliant]
    assert len(failed) >= 3  # consent, detrimental, tracking, ads


def test_master_sub_results_contains_all_clauses():
    """Master aggregator includes sub_results for each clause check."""
    record = ChildRecord(
        data_principal_age=14,
        has_verifiable_parental_consent=True,
        is_tracking_behavior=False,
        is_targeted_advertising=False,
        is_likely_to_cause_detrimental_effect=False,
    )
    r = check_child_processing(record)
    sub_sections = {sr.section for sr in r.sub_results}
    assert "Sec 9(1)" in sub_sections
    assert "Sec 9(1) proviso" in sub_sections
    assert "Sec 9(2)" in sub_sections
    assert "Sec 9(3)" in sub_sections


# ═══════════════════════════════════════════════════════════════════════════
# InvalidInputError
# ═══════════════════════════════════════════════════════════════════════════


def test_invalid_input_master():
    """Master raises InvalidInputError for non-ChildRecord input."""
    with pytest.raises(InvalidInputError) as exc:
        check_child_processing("not a ChildRecord")  # type: ignore[arg-type]
    assert "Sec 9" in str(exc.value)


def test_invalid_input_parental_consent():
    """check_parental_consent raises InvalidInputError for non-ChildRecord input."""
    with pytest.raises(InvalidInputError) as exc:
        check_parental_consent(None)  # type: ignore[arg-type]
    assert "Sec 9(1)" in str(exc.value)


def test_invalid_input_detrimental_effect():
    """check_detrimental_effect raises InvalidInputError for non-ChildRecord input."""
    with pytest.raises(InvalidInputError) as exc:
        check_detrimental_effect(None)  # type: ignore[arg-type]
    assert "Sec 9(2)" in str(exc.value)


def test_invalid_input_tracking():
    """check_tracking_prohibition raises InvalidInputError for non-ChildRecord input."""
    with pytest.raises(InvalidInputError) as exc:
        check_tracking_prohibition(None)  # type: ignore[arg-type]
    assert "Sec 9(3)" in str(exc.value)


def test_invalid_input_ads():
    """check_targeted_ads_prohibition raises InvalidInputError for non-ChildRecord input."""
    with pytest.raises(InvalidInputError) as exc:
        check_targeted_ads_prohibition(None)  # type: ignore[arg-type]
    assert "Sec 9(3)" in str(exc.value)


def test_invalid_input_class_exemption():
    """check_class_exemption raises InvalidInputError for non-ChildRecord input."""
    with pytest.raises(InvalidInputError) as exc:
        check_class_exemption(None)  # type: ignore[arg-type]
    assert "Sec 9(4)" in str(exc.value)


def test_invalid_input_age_threshold():
    """check_age_threshold_exemption raises InvalidInputError for non-ChildRecord input."""
    with pytest.raises(InvalidInputError) as exc:
        check_age_threshold_exemption(None)  # type: ignore[arg-type]
    assert "Sec 9(5)" in str(exc.value)


def test_invalid_input_disability_proviso():
    """check_disability_proviso raises InvalidInputError for non-ChildRecord input."""
    with pytest.raises(InvalidInputError) as exc:
        check_disability_proviso(None)  # type: ignore[arg-type]
    assert "Sec 9(1)" in str(exc.value)


# ═══════════════════════════════════════════════════════════════════════════
# ComplianceResult bool coercion
# ═══════════════════════════════════════════════════════════════════════════


def test_compliance_result_bool_pass():
    """Compliant result coerces to True."""
    r = check_parental_consent(_compliant_child())
    assert bool(r) is True


def test_compliance_result_bool_fail():
    """Non-compliant result coerces to False."""
    r = check_parental_consent(_non_compliant_child())
    assert bool(r) is False

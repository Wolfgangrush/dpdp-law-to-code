"""Sec 8 fiduciary test suite — covers all obligations in Sec 8(1)-(11)."""

from __future__ import annotations

import pytest

from dpdp.exceptions import InvalidInputError
from dpdp.fiduciary import (
    ErasureContext,
    check_fiduciary_compliance,
    check_fiduciary_accountability,
    check_processor_contract,
    check_data_accuracy_completeness,
    check_compliance_measures,
    check_security_safeguards,
    check_breach_notification,
    check_erasure_on_withdrawal,
    check_processor_erasure,
    check_dpo_contact_publication,
    check_grievance_mechanism,
    check_grievance_redressal,
    check_additional_obligations,
)
from dpdp.types import BreachRecord

NOW = 1_777_000_000  # May 2026 baseline
HOUR = 3_600
DAY = 86_400


# ─── helpers ───────────────────────────────────────────────────────────────

def _good_erasure() -> ErasureContext:
    return ErasureContext(
        consent_withdrawn=True,
        purpose_served=False,
        retention_required_by_law=False,
        fiduciary_erased=True,
        processor_erased=True,
    )


def _good_breach() -> BreachRecord:
    return BreachRecord(
        detected_at_unix=NOW,
        notified_board_at_unix=NOW + HOUR,
        notified_affected_principals_at_unix=NOW + 2 * HOUR,
        affected_principal_count=1_000,
        breach_description="unauthorised access to customer names and email addresses",
        contains_sensitive_categories=False,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sec 8(1) — fiduciary accountability regardless of agreement
# ═══════════════════════════════════════════════════════════════════════════

def test_sec8_1_pass():
    """Data Fiduciary acknowledges accountability regardless of agreement to contrary."""
    r = check_fiduciary_accountability(
        has_agreement_to_contrary=False,
        data_principal_accepts_charge_of_duty=False,
        processing_undertaken=True,
        processing_by_processor_on_behalf=False,
    )
    assert r.compliant is True


def test_sec8_1_pass_with_agreement_to_contrary():
    """Even with agreement to contrary, fiduciary remains accountable — accountability is non-delegable."""
    r = check_fiduciary_accountability(
        has_agreement_to_contrary=True,
        data_principal_accepts_charge_of_duty=True,
        processing_undertaken=True,
        processing_by_processor_on_behalf=False,
    )
    assert r.compliant is True


def test_sec8_1_pass_processor_on_behalf():
    """Responsibility extends to processing by Data Processor on fiduciary's behalf."""
    r = check_fiduciary_accountability(
        has_agreement_to_contrary=False,
        data_principal_accepts_charge_of_duty=False,
        processing_undertaken=True,
        processing_by_processor_on_behalf=True,
    )
    assert r.compliant is True


def test_sec8_1_fail_processor_on_behalf_not_processing():
    """Processor engaged on behalf but fiduciary not processing — inconsistent state."""
    r = check_fiduciary_accountability(
        has_agreement_to_contrary=False,
        data_principal_accepts_charge_of_duty=False,
        processing_undertaken=False,
        processing_by_processor_on_behalf=True,
    )
    assert r.compliant is False


# ═══════════════════════════════════════════════════════════════════════════
# Sec 8(2) — processor engagement only under valid contract
# ═══════════════════════════════════════════════════════════════════════════

def test_sec8_2_pass():
    """Processor engaged under valid contract."""
    r = check_processor_contract(processor_engaged=True, has_valid_contract=True)
    assert r.compliant is True


def test_sec8_2_pass_no_processor():
    """No Data Processor engaged — Sec 8(2) not triggered."""
    r = check_processor_contract(processor_engaged=False, has_valid_contract=False)
    assert r.compliant is True


def test_sec8_2_fail():
    """Processor engaged without valid contract — Sec 8(2) violation."""
    r = check_processor_contract(processor_engaged=True, has_valid_contract=False)
    assert r.compliant is False


# ═══════════════════════════════════════════════════════════════════════════
# Sec 8(3) — accuracy, completeness, consistency
# ═══════════════════════════════════════════════════════════════════════════

def test_sec8_3_pass():
    """Data used for decision — all three quality dimensions met."""
    r = check_data_accuracy_completeness(
        data_likely_used_for_decision=True,
        data_is_accurate=True,
        data_is_complete=True,
        data_is_consistent=True,
    )
    assert r.compliant is True
    assert all(s.compliant for s in r.sub_results)


def test_sec8_3_pass_not_used_for_decision():
    """Data not used for decision — Sec 8(3) not triggered."""
    r = check_data_accuracy_completeness(
        data_likely_used_for_decision=False,
        data_is_accurate=False,
        data_is_complete=False,
        data_is_consistent=False,
    )
    assert r.compliant is True


def test_sec8_3_fail_not_accurate():
    """Data used for decision but not accurate."""
    r = check_data_accuracy_completeness(
        data_likely_used_for_decision=True,
        data_is_accurate=False,
        data_is_complete=True,
        data_is_consistent=True,
    )
    assert r.compliant is False
    assert not r.sub_results[0].compliant  # accuracy


def test_sec8_3_fail_all():
    """Data used for decision — all three dimensions fail."""
    r = check_data_accuracy_completeness(
        data_likely_used_for_decision=True,
        data_is_accurate=False,
        data_is_complete=False,
        data_is_consistent=False,
    )
    assert r.compliant is False
    assert not any(s.compliant for s in r.sub_results)


def test_sec8_3_fail_partial_not_complete():
    """Data accurate and consistent but not complete."""
    r = check_data_accuracy_completeness(
        data_likely_used_for_decision=True,
        data_is_accurate=True,
        data_is_complete=False,
        data_is_consistent=True,
    )
    assert r.compliant is False
    assert r.sub_results[0].compliant
    assert not r.sub_results[1].compliant
    assert r.sub_results[2].compliant


# ═══════════════════════════════════════════════════════════════════════════
# Sec 8(4) — technical + organisational measures for compliance
# ═══════════════════════════════════════════════════════════════════════════

def test_sec8_4_pass():
    """Both technical and organisational measures in place."""
    r = check_compliance_measures(
        has_technical_measures=True,
        has_organisational_measures=True,
    )
    assert r.compliant is True
    assert all(s.compliant for s in r.sub_results)


def test_sec8_4_fail_technical():
    """Technical measures missing."""
    r = check_compliance_measures(
        has_technical_measures=False,
        has_organisational_measures=True,
    )
    assert r.compliant is False
    assert not r.sub_results[0].compliant
    assert r.sub_results[1].compliant


def test_sec8_4_fail_both():
    """Neither technical nor organisational measures in place."""
    r = check_compliance_measures(
        has_technical_measures=False,
        has_organisational_measures=False,
    )
    assert r.compliant is False
    assert not any(s.compliant for s in r.sub_results)


# ═══════════════════════════════════════════════════════════════════════════
# Sec 8(5) — reasonable security safeguards (₹250cr penalty trigger)
# ═══════════════════════════════════════════════════════════════════════════

def test_sec8_5_pass():
    """All seven security safeguard dimensions met."""
    r = check_security_safeguards(
        has_technical_safeguards=True,
        has_organisational_safeguards=True,
        encrypted_at_rest=True,
        encrypted_in_transit=True,
        access_controls_in_place=True,
        has_incident_response_plan=True,
        has_regular_security_audits=True,
    )
    assert r.compliant is True
    assert len(r.sub_results) == 7
    assert all(s.compliant for s in r.sub_results)


def test_sec8_5_pass_minimum():
    """Minimum — five mandatory dimensions met; optional audits and IR plan absent."""
    r = check_security_safeguards(
        has_technical_safeguards=True,
        has_organisational_safeguards=True,
        encrypted_at_rest=True,
        encrypted_in_transit=True,
        access_controls_in_place=True,
        has_incident_response_plan=False,
        has_regular_security_audits=False,
    )
    assert r.compliant is False  # IR plan and audits fail
    mandatory = r.sub_results[:5]
    assert all(s.compliant for s in mandatory)
    assert not r.sub_results[5].compliant  # IR plan
    assert not r.sub_results[6].compliant  # audits


def test_sec8_5_fail_no_encryption():
    """No encryption at rest or in transit — critical failure."""
    r = check_security_safeguards(
        has_technical_safeguards=True,
        has_organisational_safeguards=True,
        encrypted_at_rest=False,
        encrypted_in_transit=False,
        access_controls_in_place=True,
        has_incident_response_plan=False,
        has_regular_security_audits=False,
    )
    assert r.compliant is False
    assert not r.sub_results[2].compliant  # encryption at rest
    assert not r.sub_results[3].compliant  # encryption in transit


def test_sec8_5_fail_all():
    """No safeguards at all — maximum ₹250cr penalty exposure."""
    r = check_security_safeguards(
        has_technical_safeguards=False,
        has_organisational_safeguards=False,
        encrypted_at_rest=False,
        encrypted_in_transit=False,
        access_controls_in_place=False,
        has_incident_response_plan=False,
        has_regular_security_audits=False,
    )
    assert r.compliant is False
    assert not any(s.compliant for s in r.sub_results)


# ═══════════════════════════════════════════════════════════════════════════
# Sec 8(6) — breach notification (preserved implementation)
# ═══════════════════════════════════════════════════════════════════════════

def test_sec8_6_pass():
    """Both Board and affected Data Principals notified within 72 hours."""
    r = check_breach_notification(_good_breach())
    assert r.compliant is True
    assert all(s.compliant for s in r.sub_results)


def test_sec8_6_fail_board_not_notified():
    """Board not notified — notification field is None."""
    breach = BreachRecord(
        detected_at_unix=NOW,
        notified_board_at_unix=None,
        notified_affected_principals_at_unix=NOW + HOUR,
        affected_principal_count=500,
        breach_description="unauthorised database access",
    )
    r = check_breach_notification(breach)
    assert r.compliant is False
    assert not r.sub_results[0].compliant  # board
    assert r.sub_results[1].compliant  # principals


def test_sec8_6_fail_board_late():
    """Board notified after 72-hour window."""
    breach = BreachRecord(
        detected_at_unix=NOW,
        notified_board_at_unix=NOW + 73 * HOUR,
        notified_affected_principals_at_unix=NOW + HOUR,
        affected_principal_count=500,
        breach_description="late board notification",
    )
    r = check_breach_notification(breach)
    assert r.compliant is False
    assert not r.sub_results[0].compliant


def test_sec8_6_fail_principals_not_notified():
    """Affected Data Principals not notified."""
    breach = BreachRecord(
        detected_at_unix=NOW,
        notified_board_at_unix=NOW + HOUR,
        notified_affected_principals_at_unix=None,
        affected_principal_count=100,
        breach_description="principals not notified",
    )
    r = check_breach_notification(breach)
    assert r.compliant is False
    assert r.sub_results[0].compliant
    assert not r.sub_results[1].compliant


def test_sec8_6_fail_both():
    """Neither Board nor Data Principals notified."""
    breach = BreachRecord(
        detected_at_unix=NOW,
        notified_board_at_unix=None,
        notified_affected_principals_at_unix=None,
        affected_principal_count=10_000,
        breach_description="massive breach — no notification sent",
        contains_sensitive_categories=True,
    )
    r = check_breach_notification(breach)
    assert r.compliant is False
    assert not any(s.compliant for s in r.sub_results)


def test_sec8_6_invalid_input():
    """Invalid input type raises InvalidInputError."""
    with pytest.raises(InvalidInputError):
        check_breach_notification("not a BreachRecord")


# ═══════════════════════════════════════════════════════════════════════════
# Sec 8(7)(a) — erase on consent withdrawal or purpose served
# ═══════════════════════════════════════════════════════════════════════════

def test_sec8_7_a_pass():
    """Consent withdrawn, no retention requirement, fiduciary erased."""
    r = check_erasure_on_withdrawal(_good_erasure())
    assert r.compliant is True


def test_sec8_7_a_pass_purpose_served():
    """Purpose served, consent not withdrawn — fiduciary erased."""
    ctx = ErasureContext(
        consent_withdrawn=False,
        purpose_served=True,
        retention_required_by_law=False,
        fiduciary_erased=True,
        processor_erased=False,
    )
    r = check_erasure_on_withdrawal(ctx)
    assert r.compliant is True


def test_sec8_7_a_pass_retention_required():
    """Retention required by law — erasure obligation overridden."""
    ctx = ErasureContext(
        consent_withdrawn=True,
        purpose_served=True,
        retention_required_by_law=True,
        fiduciary_erased=False,
        processor_erased=False,
    )
    r = check_erasure_on_withdrawal(ctx)
    assert r.compliant is True


def test_sec8_7_a_pass_not_triggered():
    """Consent not withdrawn and purpose still being served — erasure not yet required."""
    ctx = ErasureContext(
        consent_withdrawn=False,
        purpose_served=False,
        retention_required_by_law=False,
        fiduciary_erased=False,
        processor_erased=False,
    )
    r = check_erasure_on_withdrawal(ctx)
    assert r.compliant is True


def test_sec8_7_a_fail():
    """Consent withdrawn but fiduciary did not erase — violation."""
    ctx = ErasureContext(
        consent_withdrawn=True,
        purpose_served=False,
        retention_required_by_law=False,
        fiduciary_erased=False,
        processor_erased=False,
    )
    r = check_erasure_on_withdrawal(ctx)
    assert r.compliant is False


def test_sec8_7_a_invalid_input():
    """Invalid input type raises InvalidInputError."""
    with pytest.raises(InvalidInputError):
        check_erasure_on_withdrawal("not an ErasureContext")


# ═══════════════════════════════════════════════════════════════════════════
# Sec 8(7)(b) — cause Data Processor to erase
# ═══════════════════════════════════════════════════════════════════════════

def test_sec8_7_b_pass():
    """Fiduciary erased and caused processor to erase."""
    r = check_processor_erasure(_good_erasure())
    assert r.compliant is True


def test_sec8_7_b_pass_retention_required():
    """Retention required by law — processor cascade not triggered."""
    ctx = ErasureContext(
        consent_withdrawn=True,
        purpose_served=True,
        retention_required_by_law=True,
        fiduciary_erased=False,
        processor_erased=False,
    )
    r = check_processor_erasure(ctx)
    assert r.compliant is True


def test_sec8_7_b_pass_not_triggered():
    """Erasure not yet required — processor cascade not triggered."""
    ctx = ErasureContext(
        consent_withdrawn=False,
        purpose_served=False,
        retention_required_by_law=False,
        fiduciary_erased=False,
        processor_erased=False,
    )
    r = check_processor_erasure(ctx)
    assert r.compliant is True


def test_sec8_7_b_fail_processor_not_erased():
    """Fiduciary erased but processor did not erase — cascading failure."""
    ctx = ErasureContext(
        consent_withdrawn=True,
        purpose_served=False,
        retention_required_by_law=False,
        fiduciary_erased=True,
        processor_erased=False,
    )
    r = check_processor_erasure(ctx)
    assert r.compliant is False


def test_sec8_7_b_fail_fiduciary_not_erased():
    """Fiduciary has not erased — cannot cascade to processor."""
    ctx = ErasureContext(
        consent_withdrawn=True,
        purpose_served=False,
        retention_required_by_law=False,
        fiduciary_erased=False,
        processor_erased=True,
    )
    r = check_processor_erasure(ctx)
    assert r.compliant is False


def test_sec8_7_b_invalid_input():
    """Invalid input type raises InvalidInputError."""
    with pytest.raises(InvalidInputError):
        check_processor_erasure("not an ErasureContext")


# ═══════════════════════════════════════════════════════════════════════════
# Sec 8(8) — publish DPO / authorised person business contact
# ═══════════════════════════════════════════════════════════════════════════

def test_sec8_8_pass():
    """DPO contact published in prescribed manner."""
    r = check_dpo_contact_publication(
        dpo_contact_published=True,
        contact_in_prescribed_manner=True,
    )
    assert r.compliant is True
    assert all(s.compliant for s in r.sub_results)


def test_sec8_8_pass_published_but_manner_unverified():
    """Contact published but manner not verified against prescribed format."""
    r = check_dpo_contact_publication(
        dpo_contact_published=True,
        contact_in_prescribed_manner=False,
    )
    assert r.compliant is False  # manner sub-check fails
    assert r.sub_results[0].compliant
    assert not r.sub_results[1].compliant


def test_sec8_8_fail():
    """DPO contact not published at all — Sec 8(8) violation."""
    r = check_dpo_contact_publication(
        dpo_contact_published=False,
        contact_in_prescribed_manner=False,
    )
    assert r.compliant is False
    assert not any(s.compliant for s in r.sub_results)


# ═══════════════════════════════════════════════════════════════════════════
# Sec 8(9) — effective grievance redressal mechanism
# ═══════════════════════════════════════════════════════════════════════════

def test_sec8_9_pass():
    """Effective grievance mechanism established, accessible to Data Principals."""
    r = check_grievance_mechanism(
        mechanism_established=True,
        mechanism_is_effective=True,
        mechanism_accessible_to_principals=True,
    )
    assert r.compliant is True
    assert all(s.compliant for s in r.sub_results)


def test_sec8_9_fail_not_established():
    """No grievance redressal mechanism established at all."""
    r = check_grievance_mechanism(
        mechanism_established=False,
        mechanism_is_effective=False,
        mechanism_accessible_to_principals=False,
    )
    assert r.compliant is False
    assert not any(s.compliant for s in r.sub_results)


def test_sec8_9_fail_not_effective():
    """Mechanism established but not effective — no tracking or resolution metrics."""
    r = check_grievance_mechanism(
        mechanism_established=True,
        mechanism_is_effective=False,
        mechanism_accessible_to_principals=True,
    )
    assert r.compliant is False
    assert r.sub_results[0].compliant
    assert not r.sub_results[1].compliant
    assert r.sub_results[2].compliant


def test_sec8_9_fail_not_accessible():
    """Mechanism established but not accessible to Data Principals."""
    r = check_grievance_mechanism(
        mechanism_established=True,
        mechanism_is_effective=True,
        mechanism_accessible_to_principals=False,
    )
    assert r.compliant is False
    assert r.sub_results[0].compliant
    assert r.sub_results[1].compliant
    assert not r.sub_results[2].compliant


# ═══════════════════════════════════════════════════════════════════════════
# Sec 8(10) — respond to grievances within prescribed period (30-day heuristic)
# ═══════════════════════════════════════════════════════════════════════════

def test_sec8_10_pass():
    """Grievance responded to within 30-day prescribed period."""
    r = check_grievance_redressal(
        grievance_received_at_unix=NOW,
        grievance_responded_at_unix=NOW + 15 * DAY,
        resolution_period_days=30,
    )
    assert r.compliant is True


def test_sec8_10_pass_exactly_30_days():
    """Grievance responded to exactly at 30-day boundary."""
    r = check_grievance_redressal(
        grievance_received_at_unix=NOW,
        grievance_responded_at_unix=NOW + 30 * DAY,
        resolution_period_days=30,
    )
    assert r.compliant is True


def test_sec8_10_fail_late():
    """Grievance responded to after 30-day period."""
    r = check_grievance_redressal(
        grievance_received_at_unix=NOW,
        grievance_responded_at_unix=NOW + 31 * DAY,
        resolution_period_days=30,
    )
    assert r.compliant is False


def test_sec8_10_fail_not_responded():
    """Grievance never responded to."""
    r = check_grievance_redressal(
        grievance_received_at_unix=NOW,
        grievance_responded_at_unix=None,
        resolution_period_days=30,
    )
    assert r.compliant is False


def test_sec8_10_custom_resolution_period():
    """Custom resolution period — 7 days for expedited grievances."""
    r = check_grievance_redressal(
        grievance_received_at_unix=NOW,
        grievance_responded_at_unix=NOW + 5 * DAY,
        resolution_period_days=7,
    )
    assert r.compliant is True

    r_late = check_grievance_redressal(
        grievance_received_at_unix=NOW,
        grievance_responded_at_unix=NOW + 8 * DAY,
        resolution_period_days=7,
    )
    assert r_late.compliant is False


# ═══════════════════════════════════════════════════════════════════════════
# Sec 8(11) — Central Government may notify additional obligations
# ═══════════════════════════════════════════════════════════════════════════

def test_sec8_11_pass_no_obligations():
    """No additional obligations notified — Sec 8(11) not triggered."""
    r = check_additional_obligations(
        additional_obligations_notified=[],
        all_obligations_complied=True,
    )
    assert r.compliant is True


def test_sec8_11_pass_none():
    """None passed as obligations list — treated as empty."""
    r = check_additional_obligations(
        additional_obligations_notified=None,
        all_obligations_complied=True,
    )
    assert r.compliant is True


def test_sec8_11_pass_all_complied():
    """Additional obligations notified and all complied with."""
    r = check_additional_obligations(
        additional_obligations_notified=[
            "appoint independent data auditor",
            "conduct DPIA annually",
            "maintain processing records for 7 years",
        ],
        all_obligations_complied=True,
    )
    assert r.compliant is True


def test_sec8_11_fail():
    """Additional obligations notified but not all complied with — Sec 8(11) violation."""
    r = check_additional_obligations(
        additional_obligations_notified=[
            "appoint independent data auditor",
            "conduct DPIA annually",
        ],
        all_obligations_complied=False,
    )
    assert r.compliant is False


# ═══════════════════════════════════════════════════════════════════════════
# Master compliance aggregator — check_fiduciary_compliance
# ═══════════════════════════════════════════════════════════════════════════

def test_master_compliance_pass():
    """All Sec 8 obligations met with fully compliant parameters."""
    r = check_fiduciary_compliance(
        has_incident_response_plan=True,
        has_regular_security_audits=True,
        contact_in_prescribed_manner=True,
        grievance_mechanism_effective=True,
        grievance_mechanism_accessible=True,
        erasure=_good_erasure(),
        grievance_received_at_unix=NOW,
        grievance_responded_at_unix=NOW + 15 * DAY,
    )
    assert r.compliant is True
    # 11 sub-results: 8(1), 8(2), 8(3), 8(4), 8(5), 8(7)(a), 8(7)(b), 8(8), 8(9), 8(10), 8(11)
    assert len(r.sub_results) == 11
    assert all(s.compliant for s in r.sub_results)


def test_master_compliance_fail_no_encryption():
    """Encryption at rest and in transit disabled — Sec 8(5) failures propagate."""
    r = check_fiduciary_compliance(
        encrypted_at_rest=False,
        encrypted_in_transit=False,
        erasure=_good_erasure(),
        grievance_received_at_unix=NOW,
        grievance_responded_at_unix=NOW + 15 * DAY,
    )
    assert r.compliant is False
    sec8_5 = [s for s in r.sub_results if s.section == "Sec 8(5)"]
    assert len(sec8_5) == 1
    assert not sec8_5[0].compliant


def test_master_compliance_fail_no_security_safeguards():
    """All security safeguards absent — maximum penalty exposure."""
    r = check_fiduciary_compliance(
        has_technical_safeguards=False,
        has_organisational_safeguards=False,
        encrypted_at_rest=False,
        encrypted_in_transit=False,
        access_controls_in_place=False,
        has_incident_response_plan=False,
        has_regular_security_audits=False,
        erasure=_good_erasure(),
        grievance_received_at_unix=NOW,
        grievance_responded_at_unix=NOW + 15 * DAY,
    )
    assert r.compliant is False


def test_master_compliance_fail_processor_no_contract():
    """Processor engaged without valid contract — Sec 8(2) failure."""
    r = check_fiduciary_compliance(
        processor_engaged=True,
        has_valid_processor_contract=False,
        erasure=_good_erasure(),
        grievance_received_at_unix=NOW,
        grievance_responded_at_unix=NOW + 15 * DAY,
    )
    assert r.compliant is False
    sec8_2 = [s for s in r.sub_results if s.section == "Sec 8(2)"]
    assert not sec8_2[0].compliant


def test_master_compliance_fail_erasure():
    """Consent withdrawn but fiduciary failed to erase — Sec 8(7) failures."""
    bad_erasure = ErasureContext(
        consent_withdrawn=True,
        purpose_served=False,
        retention_required_by_law=False,
        fiduciary_erased=False,
        processor_erased=False,
    )
    r = check_fiduciary_compliance(
        erasure=bad_erasure,
        grievance_received_at_unix=NOW,
        grievance_responded_at_unix=NOW + 15 * DAY,
    )
    assert r.compliant is False
    sec8_7a = [s for s in r.sub_results if s.section == "Sec 8(7)(a)"]
    sec8_7b = [s for s in r.sub_results if s.section == "Sec 8(7)(b)"]
    assert not sec8_7a[0].compliant


def test_master_compliance_fail_multiple():
    """Multiple failures across different sub-sections."""
    bad_erasure = ErasureContext(
        consent_withdrawn=True,
        purpose_served=False,
        retention_required_by_law=False,
        fiduciary_erased=False,
        processor_erased=False,
    )
    r = check_fiduciary_compliance(
        processor_engaged=True,
        has_valid_processor_contract=False,
        data_likely_used_for_decision=True,
        data_is_accurate=False,
        data_is_complete=False,
        data_is_consistent=False,
        has_technical_measures=False,
        encrypted_at_rest=False,
        encrypted_in_transit=False,
        dpo_contact_published=False,
        grievance_mechanism_established=False,
        grievance_responded_at_unix=None,
        additional_obligations_notified=["report quarterly"],
        all_additional_obligations_complied=False,
        erasure=bad_erasure,
    )
    assert r.compliant is False
    assert len([s for s in r.sub_results if not s.compliant]) >= 8


def test_master_compliance_no_erasure_context():
    """Erasure context omitted — Sec 8(7) checks skipped."""
    r = check_fiduciary_compliance(
        has_incident_response_plan=True,
        has_regular_security_audits=True,
        contact_in_prescribed_manner=True,
        grievance_mechanism_effective=True,
        grievance_mechanism_accessible=True,
        erasure=None,
        grievance_received_at_unix=NOW,
        grievance_responded_at_unix=NOW + 15 * DAY,
    )
    # 9 sub-results without erasure: 8(1), 8(2), 8(3), 8(4), 8(5), 8(8), 8(9), 8(10), 8(11)
    assert len(r.sub_results) == 9
    assert r.compliant is True

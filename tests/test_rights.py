"""Tests for dpdp.rights — Sec 11-14 Data Principal Rights.

Covers:
  - Sec 11: access to information (5 atomic obligations)
  - Sec 12: correction, completion, updating, erasure (9 atomic obligations)
  - Sec 13: grievance redressal (4 atomic obligations)
  - Sec 14: nomination (3 atomic obligations)
  - check_rights_response (preserved existing)
  - InvalidInputError on wrong input type
"""

from __future__ import annotations

import pytest

from dpdp.exceptions import InvalidInputError
from dpdp.rights import (
    check_rights_response,
    check_sec_11,
    check_sec_11_1_a_summary,
    check_sec_11_1_b_description,
    check_sec_11_1_b_identities,
    check_sec_11_1_c_other_info,
    check_sec_11_2_law_enforcement_exemption,
    check_sec_12,
    check_sec_12_1_completion,
    check_sec_12_1_correction,
    check_sec_12_1_erasure,
    check_sec_12_1_updating,
    check_sec_12_2_a_correction_duty,
    check_sec_12_2_b_completion_duty,
    check_sec_12_2_c_updating_duty,
    check_sec_12_3_erasure_duty,
    check_sec_13,
    check_sec_13_1_mechanism_available,
    check_sec_13_2_response_period,
    check_sec_13_3_exhaustion_required,
    check_sec_14,
    check_sec_14_1_nomination,
    check_sec_14_2_incapacity_definition,
)
from dpdp.types import ComplianceResult, RightsRequest, RightType


# ─── helpers ─────────────────────────────────────────────────────────────

def _access_request(**overrides) -> RightsRequest:
    defaults = dict(
        right=RightType.ACCESS_AND_INFORMATION,
        received_at_unix=1_000_000,
        responded_at_unix=1_001_000,
        grievance_resolution_period_days=30,
    )
    defaults.update(overrides)
    return RightsRequest(**defaults)


def _grievance_request(**overrides) -> RightsRequest:
    defaults = dict(
        right=RightType.GRIEVANCE_REDRESSAL,
        received_at_unix=1_000_000,
        responded_at_unix=1_001_000,
        grievance_resolution_period_days=30,
    )
    defaults.update(overrides)
    return RightsRequest(**defaults)


# ═══════════════════════════════════════════════════════════════════════════
# check_rights_response (preserved existing)
# ═══════════════════════════════════════════════════════════════════════════

class TestCheckRightsResponse:
    def test_pass_within_window(self):
        req = _access_request(received_at_unix=1_000_000, responded_at_unix=1_000_000 + 10 * 86400)
        r = check_rights_response(req)
        assert r.compliant is True
        assert "within 30-day window" in r.reason

    def test_fail_exceeds_window(self):
        req = _access_request(received_at_unix=1_000_000, responded_at_unix=1_000_000 + 40 * 86400)
        r = check_rights_response(req)
        assert r.compliant is False
        assert "exceeds 30-day window" in r.reason

    def test_fail_no_response(self):
        req = _access_request(responded_at_unix=None)
        r = check_rights_response(req)
        assert r.compliant is False
        assert "no response recorded" in r.reason

    def test_invalid_input_raises(self):
        with pytest.raises(InvalidInputError, match="expected RightsRequest"):
            check_rights_response("not-a-request")  # type: ignore[arg-type]

    def test_section_mapping_for_each_right_type(self):
        for right, expected_section in [
            (RightType.ACCESS_AND_INFORMATION, "Sec 11"),
            (RightType.CORRECTION_AND_ERASURE, "Sec 12"),
            (RightType.GRIEVANCE_REDRESSAL, "Sec 13"),
            (RightType.NOMINATION, "Sec 14"),
        ]:
            req = RightsRequest(right=right, received_at_unix=1_000_000, responded_at_unix=1_000_000 + 5 * 86400)
            r = check_rights_response(req)
            assert r.section == expected_section


# ═══════════════════════════════════════════════════════════════════════════
# Sec 11(1)(a) — summary of personal data + processing activities
# ═══════════════════════════════════════════════════════════════════════════

class TestSec11_1_a:
    def test_pass_both_provided(self):
        r = check_sec_11_1_a_summary(summary_provided=True, processing_activities_disclosed=True)
        assert r.compliant is True
        assert r.section == "Sec 11(1)(a)"
        assert "summary of personal data and processing activities provided" in r.reason

    def test_fail_summary_missing(self):
        r = check_sec_11_1_a_summary(summary_provided=False, processing_activities_disclosed=True)
        assert r.compliant is False
        assert "summary of personal data not provided" in r.reason

    def test_fail_activities_missing(self):
        r = check_sec_11_1_a_summary(summary_provided=True, processing_activities_disclosed=False)
        assert r.compliant is False
        assert "processing activities not disclosed" in r.reason

    def test_fail_both_missing(self):
        r = check_sec_11_1_a_summary(summary_provided=False, processing_activities_disclosed=False)
        assert r.compliant is False
        assert "summary of personal data not provided" in r.reason
        assert "processing activities not disclosed" in r.reason


# ═══════════════════════════════════════════════════════════════════════════
# Sec 11(1)(b) — identities of Fiduciaries/Processors
# ═══════════════════════════════════════════════════════════════════════════

class TestSec11_1_b_Identities:
    def test_pass_specific_identities_listed(self):
        r = check_sec_11_1_b_identities(identities_listed=True, generic_third_party_label_used=False)
        assert r.compliant is True
        assert "specific identities" in r.reason

    def test_fail_no_identities_listed(self):
        r = check_sec_11_1_b_identities(identities_listed=False, generic_third_party_label_used=False)
        assert r.compliant is False
        assert "not listed" in r.reason

    def test_fail_generic_label_used(self):
        """User asks for sub-processor names; Fiduciary lists 'third party partners'."""
        r = check_sec_11_1_b_identities(identities_listed=True, generic_third_party_label_used=True)
        assert r.compliant is False
        assert "generic third-party label" in r.reason


# ═══════════════════════════════════════════════════════════════════════════
# Sec 11(1)(b) — description of shared data
# ═══════════════════════════════════════════════════════════════════════════

class TestSec11_1_b_Description:
    def test_pass_description_provided(self):
        r = check_sec_11_1_b_description(description_of_shared_data_provided=True)
        assert r.compliant is True
        assert "description of shared data provided" in r.reason

    def test_fail_description_not_provided(self):
        r = check_sec_11_1_b_description(description_of_shared_data_provided=False)
        assert r.compliant is False
        assert "description of data shared" in r.reason


# ═══════════════════════════════════════════════════════════════════════════
# Sec 11(1)(c) — other prescribed information
# ═══════════════════════════════════════════════════════════════════════════

class TestSec11_1_c:
    def test_pass_other_info_provided(self):
        r = check_sec_11_1_c_other_info(other_prescribed_info_provided=True)
        assert r.compliant is True
        assert "other prescribed processing information provided" in r.reason

    def test_fail_other_info_not_provided(self):
        r = check_sec_11_1_c_other_info(other_prescribed_info_provided=False)
        assert r.compliant is False
        assert "other prescribed information" in r.reason


# ═══════════════════════════════════════════════════════════════════════════
# Sec 11(2) — law enforcement exemption
# ═══════════════════════════════════════════════════════════════════════════

class TestSec11_2:
    def test_pass_exemption_applies(self):
        """Bank shares data with CERT-In under directive; exemption valid."""
        r = check_sec_11_2_law_enforcement_exemption(sharing_authorised_by_law=True)
        assert r.compliant is True
        assert "sharing authorised by law" in r.reason

    def test_exemption_noted_even_when_not_authorised(self):
        """Voluntary sharing for marketing — exemption not available."""
        r = check_sec_11_2_law_enforcement_exemption(sharing_authorised_by_law=False)
        assert r.compliant is True  # always compliant — this is a carve-out check, not a violation check
        assert "exemption not available" in r.reason


# ═══════════════════════════════════════════════════════════════════════════
# Sec 11 master aggregator
# ═══════════════════════════════════════════════════════════════════════════

class TestSec11Master:
    def _all_pass_args(self):
        return dict(
            summary_provided=True,
            processing_activities_disclosed=True,
            identities_listed=True,
            generic_third_party_label_used=False,
            description_of_shared_data_provided=True,
            other_prescribed_info_provided=True,
            sharing_authorised_by_law=True,
        )

    def test_pass_all_obligations_satisfied(self):
        r = check_sec_11(**self._all_pass_args())
        assert r.compliant is True
        assert "all Sec 11 access-right obligations satisfied" in r.reason
        assert len(r.sub_results) == 5

    def test_fail_when_summary_missing(self):
        args = self._all_pass_args()
        args["summary_provided"] = False
        r = check_sec_11(**args)
        assert r.compliant is False
        assert "one or more Sec 11 access-right obligations not satisfied" in r.reason

    def test_law_enforcement_exemption_waives_identities_and_description(self):
        """When sharing is authorised by law, 11(1)(b)/(c) obligations are waived."""
        args = self._all_pass_args()
        args["identities_listed"] = False  # would normally fail
        args["description_of_shared_data_provided"] = False  # would normally fail
        args["other_prescribed_info_provided"] = False  # would normally fail
        args["sharing_authorised_by_law"] = True
        r = check_sec_11(**args)
        assert r.compliant is True  # exemption waives sub-obligations

    def test_fail_generic_label_without_exemption(self):
        args = self._all_pass_args()
        args["sharing_authorised_by_law"] = False
        args["generic_third_party_label_used"] = True
        r = check_sec_11(**args)
        assert r.compliant is False

    def test_sub_results_count_with_exemption(self):
        r = check_sec_11(**self._all_pass_args())
        assert len(r.sub_results) == 5

    def test_sub_results_count_without_exemption(self):
        args = self._all_pass_args()
        args["sharing_authorised_by_law"] = False
        r = check_sec_11(**args)
        assert len(r.sub_results) == 5


# ═══════════════════════════════════════════════════════════════════════════
# Sec 12(1) — right to correction
# ═══════════════════════════════════════════════════════════════════════════

class TestSec12_1_Correction:
    def test_pass_correction_provided(self):
        r = check_sec_12_1_correction(correction_requested=True, correction_provided=True)
        assert r.compliant is True
        assert "correction of personal data provided" in r.reason

    def test_fail_correction_denied(self):
        r = check_sec_12_1_correction(correction_requested=True, correction_provided=False)
        assert r.compliant is False
        assert "requested but not provided" in r.reason

    def test_pass_not_requested(self):
        r = check_sec_12_1_correction(correction_requested=False, correction_provided=False)
        assert r.compliant is True
        assert "right not exercised" in r.reason


# ═══════════════════════════════════════════════════════════════════════════
# Sec 12(1) — right to completion
# ═══════════════════════════════════════════════════════════════════════════

class TestSec12_1_Completion:
    def test_pass_completion_provided(self):
        r = check_sec_12_1_completion(completion_requested=True, completion_provided=True)
        assert r.compliant is True
        assert "completion of incomplete personal data provided" in r.reason

    def test_fail_completion_denied(self):
        r = check_sec_12_1_completion(completion_requested=True, completion_provided=False)
        assert r.compliant is False
        assert "requested but not provided" in r.reason

    def test_pass_not_requested(self):
        r = check_sec_12_1_completion(completion_requested=False, completion_provided=False)
        assert r.compliant is True
        assert "right not exercised" in r.reason


# ═══════════════════════════════════════════════════════════════════════════
# Sec 12(1) — right to updating
# ═══════════════════════════════════════════════════════════════════════════

class TestSec12_1_Updating:
    def test_pass_updating_provided(self):
        r = check_sec_12_1_updating(updating_requested=True, updating_provided=True)
        assert r.compliant is True
        assert "updating of personal data provided" in r.reason

    def test_fail_updating_denied(self):
        r = check_sec_12_1_updating(updating_requested=True, updating_provided=False)
        assert r.compliant is False
        assert "requested but not provided" in r.reason

    def test_pass_not_requested(self):
        r = check_sec_12_1_updating(updating_requested=False, updating_provided=False)
        assert r.compliant is True
        assert "right not exercised" in r.reason


# ═══════════════════════════════════════════════════════════════════════════
# Sec 12(1) — right to erasure
# ═══════════════════════════════════════════════════════════════════════════

class TestSec12_1_Erasure:
    def test_pass_erasure_carried_out(self):
        r = check_sec_12_1_erasure(erasure_requested=True, erasure_provided=True)
        assert r.compliant is True
        assert "erasure of personal data carried out" in r.reason

    def test_fail_erasure_not_carried_out(self):
        r = check_sec_12_1_erasure(erasure_requested=True, erasure_provided=False)
        assert r.compliant is False
        assert "requested but not carried out" in r.reason

    def test_pass_not_requested(self):
        r = check_sec_12_1_erasure(erasure_requested=False, erasure_provided=False)
        assert r.compliant is True
        assert "right not exercised" in r.reason

    def test_pass_retention_required_by_law(self):
        r = check_sec_12_1_erasure(
            erasure_requested=True, erasure_provided=False,
            retention_required_by_law=True, retention_necessary_for_purpose=False,
        )
        assert r.compliant is True
        assert "retention required by law" in r.reason

    def test_pass_retention_necessary_for_purpose(self):
        r = check_sec_12_1_erasure(
            erasure_requested=True, erasure_provided=False,
            retention_required_by_law=False, retention_necessary_for_purpose=True,
        )
        assert r.compliant is True
        assert "retention necessary for specified purpose" in r.reason

    def test_fail_no_exception_applies(self):
        r = check_sec_12_1_erasure(
            erasure_requested=True, erasure_provided=False,
            retention_required_by_law=False, retention_necessary_for_purpose=False,
        )
        assert r.compliant is False
        assert "no lawful retention exception" in r.reason


# ═══════════════════════════════════════════════════════════════════════════
# Sec 12(2)(a) — fiduciary correction duty
# ═══════════════════════════════════════════════════════════════════════════

class TestSec12_2_a:
    def test_pass_fiduciary_corrected_inaccurate_data(self):
        r = check_sec_12_2_a_correction_duty(
            correction_requested=True, fiduciary_corrected=True, data_was_inaccurate_or_misleading=True,
        )
        assert r.compliant is True
        assert "Fiduciary corrected" in r.reason

    def test_fail_fiduciary_refused_to_correct(self):
        """User requests email correction; Fiduciary refuses."""
        r = check_sec_12_2_a_correction_duty(
            correction_requested=True, fiduciary_corrected=False, data_was_inaccurate_or_misleading=True,
        )
        assert r.compliant is False
        assert "failed to correct" in r.reason

    def test_pass_not_requested(self):
        r = check_sec_12_2_a_correction_duty(
            correction_requested=False, fiduciary_corrected=False, data_was_inaccurate_or_misleading=True,
        )
        assert r.compliant is True
        assert "not requested" in r.reason

    def test_pass_data_not_inaccurate(self):
        r = check_sec_12_2_a_correction_duty(
            correction_requested=True, fiduciary_corrected=False, data_was_inaccurate_or_misleading=False,
        )
        assert r.compliant is True
        assert "not inaccurate or misleading" in r.reason


# ═══════════════════════════════════════════════════════════════════════════
# Sec 12(2)(b) — fiduciary completion duty
# ═══════════════════════════════════════════════════════════════════════════

class TestSec12_2_b:
    def test_pass_fiduciary_completed_incomplete_data(self):
        r = check_sec_12_2_b_completion_duty(
            completion_requested=True, fiduciary_completed=True, data_was_incomplete=True,
        )
        assert r.compliant is True
        assert "Fiduciary completed" in r.reason

    def test_fail_fiduciary_refused_to_complete(self):
        r = check_sec_12_2_b_completion_duty(
            completion_requested=True, fiduciary_completed=False, data_was_incomplete=True,
        )
        assert r.compliant is False
        assert "failed to complete" in r.reason

    def test_pass_not_requested(self):
        r = check_sec_12_2_b_completion_duty(
            completion_requested=False, fiduciary_completed=False, data_was_incomplete=True,
        )
        assert r.compliant is True
        assert "not requested" in r.reason

    def test_pass_data_not_incomplete(self):
        r = check_sec_12_2_b_completion_duty(
            completion_requested=True, fiduciary_completed=False, data_was_incomplete=False,
        )
        assert r.compliant is True
        assert "not incomplete" in r.reason


# ═══════════════════════════════════════════════════════════════════════════
# Sec 12(2)(c) — fiduciary updating duty
# ═══════════════════════════════════════════════════════════════════════════

class TestSec12_2_c:
    def test_pass_fiduciary_updated(self):
        r = check_sec_12_2_c_updating_duty(updating_requested=True, fiduciary_updated=True)
        assert r.compliant is True
        assert "Fiduciary updated" in r.reason

    def test_fail_fiduciary_refused_to_update(self):
        r = check_sec_12_2_c_updating_duty(updating_requested=True, fiduciary_updated=False)
        assert r.compliant is False
        assert "failed to update" in r.reason

    def test_pass_not_requested(self):
        r = check_sec_12_2_c_updating_duty(updating_requested=False, fiduciary_updated=False)
        assert r.compliant is True
        assert "not requested" in r.reason


# ═══════════════════════════════════════════════════════════════════════════
# Sec 12(3) — fiduciary erasure duty with exceptions
# ═══════════════════════════════════════════════════════════════════════════

class TestSec12_3:
    def test_pass_fiduciary_erased(self):
        r = check_sec_12_3_erasure_duty(
            erasure_requested=True, fiduciary_erased=True,
            retention_required_by_law=False, retention_necessary_for_purpose=False,
        )
        assert r.compliant is True
        assert "erased personal data on request" in r.reason

    def test_pass_retention_required_by_law(self):
        """User requests erasure; Fiduciary retains under Tax Act mandate."""
        r = check_sec_12_3_erasure_duty(
            erasure_requested=True, fiduciary_erased=False,
            retention_required_by_law=True, retention_necessary_for_purpose=False,
        )
        assert r.compliant is True
        assert "retention required by law" in r.reason

    def test_pass_retention_necessary_for_purpose(self):
        r = check_sec_12_3_erasure_duty(
            erasure_requested=True, fiduciary_erased=False,
            retention_required_by_law=False, retention_necessary_for_purpose=True,
        )
        assert r.compliant is True
        assert "retention necessary for specified purpose" in r.reason

    def test_fail_no_lawful_exception(self):
        r = check_sec_12_3_erasure_duty(
            erasure_requested=True, fiduciary_erased=False,
            retention_required_by_law=False, retention_necessary_for_purpose=False,
        )
        assert r.compliant is False
        assert "no lawful retention exception" in r.reason

    def test_pass_not_requested(self):
        r = check_sec_12_3_erasure_duty(
            erasure_requested=False, fiduciary_erased=False,
            retention_required_by_law=False, retention_necessary_for_purpose=False,
        )
        assert r.compliant is True
        assert "not requested" in r.reason

    def test_both_exceptions_true_erasure_not_done_still_compliant(self):
        r = check_sec_12_3_erasure_duty(
            erasure_requested=True, fiduciary_erased=False,
            retention_required_by_law=True, retention_necessary_for_purpose=True,
        )
        assert r.compliant is True


# ═══════════════════════════════════════════════════════════════════════════
# Sec 12 master aggregator
# ═══════════════════════════════════════════════════════════════════════════

class TestSec12Master:
    def _all_pass_args(self):
        return dict(
            correction_requested=True,
            correction_provided=True,
            completion_requested=True,
            completion_provided=True,
            updating_requested=True,
            updating_provided=True,
            erasure_requested=True,
            erasure_provided=True,
            data_was_inaccurate_or_misleading=True,
            data_was_incomplete=True,
            retention_required_by_law=False,
            retention_necessary_for_purpose=False,
        )

    def test_pass_all_obligations_satisfied(self):
        r = check_sec_12(**self._all_pass_args())
        assert r.compliant is True
        assert "all Sec 12 correction/erasure obligations satisfied" in r.reason
        assert len(r.sub_results) == 8

    def test_fail_correction_denied(self):
        args = self._all_pass_args()
        args["correction_provided"] = False
        r = check_sec_12(**args)
        assert r.compliant is False
        assert "one or more Sec 12 correction/erasure obligations not satisfied" in r.reason

    def test_fail_erasure_denied_no_exception(self):
        args = self._all_pass_args()
        args["erasure_provided"] = False
        r = check_sec_12(**args)
        assert r.compliant is False

    def test_pass_all_rights_unexercised(self):
        """No rights exercised — all duties are not triggered."""
        args = dict(
            correction_requested=False, correction_provided=False,
            completion_requested=False, completion_provided=False,
            updating_requested=False, updating_provided=False,
            erasure_requested=False, erasure_provided=False,
            data_was_inaccurate_or_misleading=False,
            data_was_incomplete=False,
            retention_required_by_law=False,
            retention_necessary_for_purpose=False,
        )
        r = check_sec_12(**args)
        assert r.compliant is True

    def test_pass_erasure_not_done_but_retention_required_by_law(self):
        args = self._all_pass_args()
        args["erasure_provided"] = False
        args["retention_required_by_law"] = True
        r = check_sec_12(**args)
        assert r.compliant is True  # lawful exception

    def test_sub_results_count(self):
        r = check_sec_12(**self._all_pass_args())
        assert len(r.sub_results) == 8


# ═══════════════════════════════════════════════════════════════════════════
# Sec 13(1) — grievance mechanism available
# ═══════════════════════════════════════════════════════════════════════════

class TestSec13_1:
    def test_pass_mechanism_available(self):
        r = check_sec_13_1_mechanism_available(mechanism_available=True)
        assert r.compliant is True
        assert "readily available means" in r.reason

    def test_fail_no_mechanism(self):
        r = check_sec_13_1_mechanism_available(mechanism_available=False)
        assert r.compliant is False
        assert "no readily available means" in r.reason


# ═══════════════════════════════════════════════════════════════════════════
# Sec 13(2) — grievance response period
# ═══════════════════════════════════════════════════════════════════════════

class TestSec13_2:
    def test_pass_within_window(self):
        req = _grievance_request(received_at_unix=1_000_000, responded_at_unix=1_000_000 + 10 * 86400)
        r = check_sec_13_2_response_period(req)
        assert r.compliant is True
        assert r.section == "Sec 13(2)"
        assert "within 30-day window" in r.reason

    def test_fail_exceeds_window(self):
        """User raises grievance; Fiduciary takes 60 days."""
        req = _grievance_request(received_at_unix=1_000_000, responded_at_unix=1_000_000 + 60 * 86400)
        r = check_sec_13_2_response_period(req)
        assert r.compliant is False
        assert "exceeds 30-day window" in r.reason

    def test_fail_no_response(self):
        req = _grievance_request(responded_at_unix=None)
        r = check_sec_13_2_response_period(req)
        assert r.compliant is False
        assert "no response recorded" in r.reason

    def test_invalid_input_not_rights_request(self):
        with pytest.raises(InvalidInputError, match="expected RightsRequest"):
            check_sec_13_2_response_period("not-a-request")  # type: ignore[arg-type]

    def test_invalid_input_wrong_right_type(self):
        req = _access_request()
        with pytest.raises(InvalidInputError, match="GRIEVANCE_REDRESSAL"):
            check_sec_13_2_response_period(req)


# ═══════════════════════════════════════════════════════════════════════════
# Sec 13(3) — exhaustion of internal grievance mechanism
# ═══════════════════════════════════════════════════════════════════════════

class TestSec13_3:
    def test_pass_filed_with_fiduciary_first(self):
        r = check_sec_13_3_exhaustion_required(grievance_filed_with_fiduciary_first=True)
        assert r.compliant is True
        assert "exhaustion requirement satisfied" in r.reason

    def test_fail_skipped_fiduciary(self):
        """User skips Fiduciary mechanism, goes straight to Board."""
        r = check_sec_13_3_exhaustion_required(grievance_filed_with_fiduciary_first=False)
        assert r.compliant is False
        assert "must exhaust internal grievance mechanism" in r.reason


# ═══════════════════════════════════════════════════════════════════════════
# Sec 13 master aggregator
# ═══════════════════════════════════════════════════════════════════════════

class TestSec13Master:
    def test_pass_all_obligations_satisfied(self):
        req = _grievance_request(received_at_unix=1_000_000, responded_at_unix=1_000_000 + 10 * 86400)
        r = check_sec_13(mechanism_available=True, request=req, grievance_filed_with_fiduciary_first=True)
        assert r.compliant is True
        assert "all Sec 13 grievance-redressal obligations satisfied" in r.reason
        assert len(r.sub_results) == 3

    def test_fail_no_mechanism(self):
        req = _grievance_request(received_at_unix=1_000_000, responded_at_unix=1_000_000 + 10 * 86400)
        r = check_sec_13(mechanism_available=False, request=req, grievance_filed_with_fiduciary_first=True)
        assert r.compliant is False

    def test_fail_late_response(self):
        req = _grievance_request(received_at_unix=1_000_000, responded_at_unix=1_000_000 + 60 * 86400)
        r = check_sec_13(mechanism_available=True, request=req, grievance_filed_with_fiduciary_first=True)
        assert r.compliant is False

    def test_fail_skipped_fiduciary(self):
        req = _grievance_request(received_at_unix=1_000_000, responded_at_unix=1_000_000 + 10 * 86400)
        r = check_sec_13(mechanism_available=True, request=req, grievance_filed_with_fiduciary_first=False)
        assert r.compliant is False

    def test_invalid_input_not_rights_request(self):
        with pytest.raises(InvalidInputError, match="expected RightsRequest"):
            check_sec_13(True, "not-a-request", True)  # type: ignore[arg-type]

    def test_all_three_fail(self):
        req = _grievance_request(received_at_unix=1_000_000, responded_at_unix=1_000_000 + 60 * 86400)
        r = check_sec_13(mechanism_available=False, request=req, grievance_filed_with_fiduciary_first=False)
        assert r.compliant is False
        assert len(r.sub_results) == 3


# ═══════════════════════════════════════════════════════════════════════════
# Sec 14(1) — nomination
# ═══════════════════════════════════════════════════════════════════════════

class TestSec14_1:
    def test_pass_nominee_designated_in_prescribed_manner(self):
        r = check_sec_14_1_nomination(nominee_designated=True, manner_prescribed_followed=True)
        assert r.compliant is True
        assert "nominee designated in prescribed manner" in r.reason

    def test_fail_no_nominee(self):
        r = check_sec_14_1_nomination(nominee_designated=False, manner_prescribed_followed=False)
        assert r.compliant is False
        assert "no nominee designated" in r.reason

    def test_fail_prescribed_manner_not_followed(self):
        r = check_sec_14_1_nomination(nominee_designated=True, manner_prescribed_followed=False)
        assert r.compliant is False
        assert "manner prescribed not followed" in r.reason

    def test_fail_both_false(self):
        r = check_sec_14_1_nomination(nominee_designated=False, manner_prescribed_followed=True)
        assert r.compliant is False


# ═══════════════════════════════════════════════════════════════════════════
# Sec 14(2) — incapacity definition
# ═══════════════════════════════════════════════════════════════════════════

class TestSec14_2:
    def test_pass_incapacity_meets_definition(self):
        r = check_sec_14_2_incapacity_definition(incapacity_meets_definition=True)
        assert r.compliant is True
        assert "meets statutory definition" in r.reason

    def test_fail_incapacity_does_not_meet_definition(self):
        r = check_sec_14_2_incapacity_definition(incapacity_meets_definition=False)
        assert r.compliant is False
        assert "does not meet statutory definition" in r.reason


# ═══════════════════════════════════════════════════════════════════════════
# Sec 14 master aggregator
# ═══════════════════════════════════════════════════════════════════════════

class TestSec14Master:
    def test_pass_all_obligations_satisfied(self):
        """Nominee exercises rights after Data Principal's death with prescribed-manner nomination."""
        r = check_sec_14(
            nominee_designated=True, manner_prescribed_followed=True, incapacity_meets_definition=True,
        )
        assert r.compliant is True
        assert "all Sec 14 nomination obligations satisfied" in r.reason
        assert len(r.sub_results) == 2

    def test_fail_no_nominee(self):
        r = check_sec_14(
            nominee_designated=False, manner_prescribed_followed=False, incapacity_meets_definition=True,
        )
        assert r.compliant is False
        assert "one or more Sec 14 nomination obligations not satisfied" in r.reason

    def test_fail_incapacity_not_met(self):
        r = check_sec_14(
            nominee_designated=True, manner_prescribed_followed=True, incapacity_meets_definition=False,
        )
        assert r.compliant is False

    def test_fail_both(self):
        r = check_sec_14(
            nominee_designated=False, manner_prescribed_followed=False, incapacity_meets_definition=False,
        )
        assert r.compliant is False


# ═══════════════════════════════════════════════════════════════════════════
# Realistic scenario tests
# ═══════════════════════════════════════════════════════════════════════════

class TestRealisticScenarios:
    def test_user_asks_subprocessor_names_generic_label_fails(self):
        """User asks for sub-processor names; Fiduciary lists 'third party partners'."""
        r = check_sec_11(
            summary_provided=True,
            processing_activities_disclosed=True,
            identities_listed=True,
            generic_third_party_label_used=True,
            description_of_shared_data_provided=True,
            other_prescribed_info_provided=True,
            sharing_authorised_by_law=False,
        )
        assert r.compliant is False
        id_result = [s for s in r.sub_results if s.section == "Sec 11(1)(b)" and "generic" in s.reason]
        assert len(id_result) >= 1

    def test_bank_shares_with_cert_in_exemption(self):
        """Bank shares data with CERT-In under directive; user can't access record."""
        r = check_sec_11(
            summary_provided=True,
            processing_activities_disclosed=True,
            identities_listed=False,  # withheld
            generic_third_party_label_used=False,
            description_of_shared_data_provided=False,  # withheld
            other_prescribed_info_provided=False,  # withheld
            sharing_authorised_by_law=True,
        )
        assert r.compliant is True  # exemption waives 11(1)(b)/(c)

    def test_user_requests_email_correction_fiduciary_refuses(self):
        """User requests email correction; Fiduciary refuses."""
        r = check_sec_12_2_a_correction_duty(
            correction_requested=True, fiduciary_corrected=False, data_was_inaccurate_or_misleading=True,
        )
        assert r.compliant is False

    def test_user_requests_erasure_tax_act_retention(self):
        """User requests erasure; Fiduciary retains under Tax Act mandate."""
        r = check_sec_12_3_erasure_duty(
            erasure_requested=True, fiduciary_erased=False,
            retention_required_by_law=True, retention_necessary_for_purpose=False,
        )
        assert r.compliant is True

    def test_user_grievance_60_days_late(self):
        """User raises grievance; Fiduciary takes 60 days."""
        req = _grievance_request(received_at_unix=1_000_000, responded_at_unix=1_000_000 + 60 * 86400)
        r = check_sec_13_2_response_period(req)
        assert r.compliant is False

    def test_user_skips_fiduciary_goes_to_board(self):
        """User skips Fiduciary mechanism, goes straight to Board."""
        r = check_sec_13_3_exhaustion_required(grievance_filed_with_fiduciary_first=False)
        assert r.compliant is False

    def test_nominee_exercises_rights_after_death(self):
        """Nominee exercises rights after Data Principal's death with prescribed-manner nomination."""
        r = check_sec_14(
            nominee_designated=True, manner_prescribed_followed=True, incapacity_meets_definition=True,
        )
        assert r.compliant is True

    def test_erasure_denied_for_internal_analytics_fails(self):
        """'Internal analytics' doesn't qualify as retention-necessary-for-purpose."""
        r = check_sec_12_3_erasure_duty(
            erasure_requested=True, fiduciary_erased=False,
            retention_required_by_law=False, retention_necessary_for_purpose=False,
        )
        assert r.compliant is False
        assert "no lawful retention exception" in r.reason


# ═══════════════════════════════════════════════════════════════════════════
# InvalidInputError tests for public functions
# ═══════════════════════════════════════════════════════════════════════════

class TestInvalidInputErrors:
    """Spot-check InvalidInputError on key public functions that take non-primitive args."""

    def test_check_sec_13_master_raises_on_bad_request(self):
        with pytest.raises(InvalidInputError, match="expected RightsRequest"):
            check_sec_13(True, "not-a-request", True)  # type: ignore[arg-type]

    def test_check_sec_13_2_raises_on_wrong_type(self):
        with pytest.raises(InvalidInputError):
            check_sec_13_2_response_period("bad")  # type: ignore[arg-type]

    def test_check_rights_response_raises_on_bad_type(self):
        with pytest.raises(InvalidInputError):
            check_rights_response(None)  # type: ignore[arg-type]

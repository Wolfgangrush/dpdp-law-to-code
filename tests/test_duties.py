"""Tests for dpdp.duties — Sec 15 Duties of Data Principal."""

from __future__ import annotations

import pytest

from dpdp.duties import (
    _DUTY_PENALTY_CAP_INR,
    check_data_principal_duty,
    check_sec_15_a,
    check_sec_15_b,
    check_sec_15_c,
    check_sec_15_d,
    check_sec_15_e,
)
from dpdp.exceptions import InvalidInputError
from dpdp.types import ComplianceResult, DataPrincipalDuty

# ── helpers ────────────────────────────────────────────────────────────────


def _duty(**kwargs: bool) -> DataPrincipalDuty:
    """Build a DataPrincipalDuty with all fields defaulting False (compliant)."""
    defaults = {
        "submitted_false_particulars": False,
        "impersonated_another_person": False,
        "suppressed_material_information": False,
        "filed_frivolous_grievance": False,
        "filed_false_complaint": False,
    }
    defaults.update(kwargs)
    return DataPrincipalDuty(**defaults)


# ── Sec 15(a) ──────────────────────────────────────────────────────────────


class TestSec15A:
    def test_complies_with_applicable_laws_pass(self):
        """Data Principal complies with all applicable laws while exercising rights."""
        result = check_sec_15_a(True)
        assert result.compliant
        assert result.section == "Sec 15(a)"
        assert "complies" in result.reason.lower()

    def test_complies_with_applicable_laws_fail(self):
        """Data Principal breaches applicable laws while exercising rights."""
        result = check_sec_15_a(False)
        assert not result.compliant
        assert result.section == "Sec 15(a)"
        assert f"₹{_DUTY_PENALTY_CAP_INR:,}" in result.reason

    def test_invalid_input_raises(self):
        with pytest.raises(InvalidInputError, match="complies_with_applicable_laws must be bool"):
            check_sec_15_a(None)  # type: ignore[arg-type]


# ── Sec 15(b) ──────────────────────────────────────────────────────────────


class TestSec15B:
    def test_no_impersonation_pass(self):
        """User provides personal data under their own identity — compliant."""
        duty = _duty(impersonated_another_person=False)
        result = check_sec_15_b(duty)
        assert result.compliant
        assert result.section == "Sec 15(b)"

    def test_impersonation_fail(self):
        """User signs up using sibling's Aadhaar — impersonation breach."""
        duty = _duty(impersonated_another_person=True)
        result = check_sec_15_b(duty)
        assert not result.compliant
        assert result.section == "Sec 15(b)"
        assert "impersonated" in result.reason.lower()
        assert f"₹{_DUTY_PENALTY_CAP_INR:,}" in result.reason

    def test_invalid_input_raises(self):
        with pytest.raises(InvalidInputError, match="expected DataPrincipalDuty"):
            check_sec_15_b(None)  # type: ignore[arg-type]


# ── Sec 15(c) ──────────────────────────────────────────────────────────────


class TestSec15C:
    def test_no_suppression_no_false_particulars_pass(self):
        """Data Principal provides truthful, complete information."""
        duty = _duty()
        result = check_sec_15_c(duty)
        assert result.compliant
        assert result.section == "Sec 15(c)"

    def test_false_particulars_fail(self):
        """User submits false name on a State-issued document application."""
        duty = _duty(submitted_false_particulars=True)
        result = check_sec_15_c(duty)
        assert not result.compliant
        assert result.section == "Sec 15(c)"
        assert "false particulars" in result.reason.lower()
        assert f"₹{_DUTY_PENALTY_CAP_INR:,}" in result.reason

    def test_suppressed_material_information_fail(self):
        """User hides income for a govt subsidy application."""
        duty = _duty(suppressed_material_information=True)
        result = check_sec_15_c(duty)
        assert not result.compliant
        assert result.section == "Sec 15(c)"
        assert "suppressed material information" in result.reason.lower()
        assert f"₹{_DUTY_PENALTY_CAP_INR:,}" in result.reason

    def test_both_c_breaches_aggregated(self):
        """Both false particulars AND suppressed information — both reported."""
        duty = _duty(submitted_false_particulars=True, suppressed_material_information=True)
        result = check_sec_15_c(duty)
        assert not result.compliant
        assert len(result.sub_results) == 2
        assert any("false particulars" in r.reason for r in result.sub_results)
        assert any("suppressed" in r.reason for r in result.sub_results)

    def test_invalid_input_raises(self):
        with pytest.raises(InvalidInputError, match="expected DataPrincipalDuty"):
            check_sec_15_c(None)  # type: ignore[arg-type]


# ── Sec 15(d) ──────────────────────────────────────────────────────────────


class TestSec15D:
    def test_no_false_or_frivolous_grievance_pass(self):
        """Data Principal files legitimate grievances only."""
        duty = _duty()
        result = check_sec_15_d(duty)
        assert result.compliant
        assert result.section == "Sec 15(d)"

    def test_frivolous_grievance_fail(self):
        """User files 50 frivolous complaints — frivolous-grievance breach."""
        duty = _duty(filed_frivolous_grievance=True)
        result = check_sec_15_d(duty)
        assert not result.compliant
        assert result.section == "Sec 15(d)"
        assert "frivolous" in result.reason.lower()
        assert f"₹{_DUTY_PENALTY_CAP_INR:,}" in result.reason

    def test_false_complaint_fail(self):
        """User files a knowingly false complaint with the Board."""
        duty = _duty(filed_false_complaint=True)
        result = check_sec_15_d(duty)
        assert not result.compliant
        assert result.section == "Sec 15(d)"
        assert "false complaint" in result.reason.lower()
        assert f"₹{_DUTY_PENALTY_CAP_INR:,}" in result.reason

    def test_both_d_breaches_aggregated(self):
        """User files frivolous grievance AND false complaint — both reported."""
        duty = _duty(filed_frivolous_grievance=True, filed_false_complaint=True)
        result = check_sec_15_d(duty)
        assert not result.compliant
        assert len(result.sub_results) == 2
        assert any("frivolous" in r.reason for r in result.sub_results)
        assert any("false complaint" in r.reason for r in result.sub_results)

    def test_invalid_input_raises(self):
        with pytest.raises(InvalidInputError, match="expected DataPrincipalDuty"):
            check_sec_15_d(None)  # type: ignore[arg-type]


# ── Sec 15(e) ──────────────────────────────────────────────────────────────


class TestSec15E:
    def test_furnishes_verifiably_authentic_info_pass(self):
        """Data Principal submits authentic documents for a correction request."""
        result = check_sec_15_e(True)
        assert result.compliant
        assert result.section == "Sec 15(e)"
        assert "verifiably authentic" in result.reason.lower()

    def test_furnishes_unverifiable_info_fail(self):
        """User submits a false income certificate for a correction request — Sec 15(e) breach."""
        result = check_sec_15_e(False)
        assert not result.compliant
        assert result.section == "Sec 15(e)"
        assert "verifiably authentic" in result.reason.lower()
        assert f"₹{_DUTY_PENALTY_CAP_INR:,}" in result.reason

    def test_invalid_input_raises(self):
        with pytest.raises(InvalidInputError, match="furnishes_verifiably_authentic_information must be bool"):
            check_sec_15_e(None)  # type: ignore[arg-type]


# ── Master check_data_principal_duty ────────────────────────────────────────


class TestCheckDataPrincipalDutyMaster:
    def test_all_duties_satisfied_pass(self):
        """User exercises rights honestly + complies with all applicable laws."""
        duty = _duty()
        result = check_data_principal_duty(duty)
        assert result.compliant
        assert result.section == "Sec 15"
        assert "no Sec 15 duty breach" in result.reason
        assert len(result.sub_results) == 0

    def test_single_breach_fails_with_10k_penalty(self):
        """Impersonation alone renders the Data Principal non-compliant."""
        duty = _duty(impersonated_another_person=True)
        result = check_data_principal_duty(duty)
        assert not result.compliant
        assert result.section == "Sec 15"
        assert "1 duty breach" in result.reason
        assert f"₹{_DUTY_PENALTY_CAP_INR:,}" in result.reason
        assert len(result.sub_results) == 5  # all five sub-clauses evaluated

    def test_multiple_breaches_aggregated_with_10k_cap(self):
        """User commits multiple breaches — all aggregated under Sec 15 with penalty cap."""
        duty = _duty(
            impersonated_another_person=True,
            suppressed_material_information=True,
            filed_frivolous_grievance=True,
        )
        result = check_data_principal_duty(duty)
        assert not result.compliant
        assert "3 duty breach" in result.reason
        assert f"₹{_DUTY_PENALTY_CAP_INR:,}" in result.reason
        assert len(result.sub_results) == 5

    def test_all_five_breaches(self):
        """Every sub-clause breached — all five reported."""
        duty = _duty(
            submitted_false_particulars=True,
            impersonated_another_person=True,
            suppressed_material_information=True,
            filed_frivolous_grievance=True,
            filed_false_complaint=True,
        )
        result = check_data_principal_duty(
            duty,
            complies_with_applicable_laws=False,
            furnishes_verifiably_authentic_information=False,
        )
        assert not result.compliant
        assert "duty breach" in result.reason
        assert len(result.sub_results) == 5
        breach_count = sum(1 for r in result.sub_results if not r.compliant)
        assert breach_count == 5

    def test_sec_15_a_kwarg_defaults_to_pass(self):
        """Caller does NOT pass Sec 15(a) kwarg — defaults to compliant (non-breaking refactor)."""
        duty = _duty()
        result = check_data_principal_duty(duty)
        assert result.compliant
        assert "no Sec 15 duty breach" in result.reason
        # Verify Sec 15(a) sub-result exists and passed
        sec_15_a_results = [r for r in result.sub_results if isinstance(r, ComplianceResult) and r.section == "Sec 15(a)"]
        assert len(sec_15_a_results) == 0  # sub_results only populated on failure

    def test_sec_15_e_kwarg_defaults_to_pass(self):
        """Caller does NOT pass Sec 15(e) kwarg — defaults to compliant (non-breaking refactor)."""
        duty = _duty()
        result = check_data_principal_duty(duty)
        assert result.compliant

    def test_sec_15_a_explicit_fail_propagates_to_master(self):
        """Explicit Sec 15(a) failure appears in master sub_results."""
        duty = _duty()
        result = check_data_principal_duty(duty, complies_with_applicable_laws=False)
        assert not result.compliant
        sec_15_a_fails = [r for r in result.sub_results if r.section == "Sec 15(a)" and not r.compliant]
        assert len(sec_15_a_fails) == 1

    def test_sec_15_e_explicit_fail_propagates_to_master(self):
        """Explicit Sec 15(e) failure appears in master sub_results."""
        duty = _duty()
        result = check_data_principal_duty(duty, furnishes_verifiably_authentic_information=False)
        assert not result.compliant
        sec_15_e_fails = [r for r in result.sub_results if r.section == "Sec 15(e)" and not r.compliant]
        assert len(sec_15_e_fails) == 1

    def test_invalid_input_raises(self):
        with pytest.raises(InvalidInputError, match="expected DataPrincipalDuty"):
            check_data_principal_duty(None)  # type: ignore[arg-type]

    def test_10k_penalty_appears_in_master_reason(self):
        """Master failure reason references the ₹10,000 penalty cap."""
        duty = _duty(impersonated_another_person=True)
        result = check_data_principal_duty(duty)
        assert f"₹{_DUTY_PENALTY_CAP_INR:,}" in result.reason

    def test_sub_results_all_sections_present_when_failing(self):
        """When any breach occurs, sub_results contain all five sub-clause evaluations."""
        duty = _duty(impersonated_another_person=True)
        result = check_data_principal_duty(duty)
        sections = {r.section for r in result.sub_results}
        assert sections == {"Sec 15(a)", "Sec 15(b)", "Sec 15(c)", "Sec 15(d)", "Sec 15(e)"}

    def test_return_type_is_complianceresult(self):
        result = check_data_principal_duty(_duty())
        assert isinstance(result, ComplianceResult)

    def test_complianceresult_bool_interface(self):
        """ComplianceResult truthiness matches compliant field."""
        assert bool(check_data_principal_duty(_duty()))
        assert not bool(check_data_principal_duty(_duty(impersonated_another_person=True)))

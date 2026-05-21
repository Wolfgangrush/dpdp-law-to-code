"""Tests for dpdp.sdf — Sec 10 Significant Data Fiduciary.

Covers:
  - Sec 10(1)(a)-(f) individual factor checks
  - assess_sdf_threshold() aggregator with realistic scenarios
  - Sec 10(2)(a)-(d) individual obligation checks
  - check_sdf_obligations() aggregator with realistic scenarios
  - InvalidInputError on wrong input type
"""

from __future__ import annotations

import pytest

from dpdp.exceptions import InvalidInputError
from dpdp.sdf import (
    assess_sdf_threshold,
    check_sdf_obligations,
    check_sec_10_1_a,
    check_sec_10_1_b,
    check_sec_10_1_c,
    check_sec_10_1_d,
    check_sec_10_1_e,
    check_sec_10_1_f,
    check_sec_10_2_a_dpo,
    check_sec_10_2_b_auditor,
    check_sec_10_2_c_dpia,
    check_sec_10_2_d_other_measures,
)
from dpdp.types import ComplianceResult, SDFContext


# ─── helpers ─────────────────────────────────────────────────────────────

def _low_risk_context(**overrides) -> SDFContext:
    """Small shop with 100 records — unlikely SDF."""
    defaults = dict(
        volume_of_personal_data_processed=100,
        sensitivity_of_personal_data=0.1,
        risk_to_rights_of_data_principals=0.1,
        risk_to_sovereignty_or_integrity=0.0,
        risk_to_electoral_democracy=0.0,
        risk_to_state_security=0.0,
        risk_to_public_order=0.0,
        notified_as_sdf_by_central_govt=False,
        has_appointed_dpo=False,
        has_appointed_data_auditor=False,
        conducts_periodic_dpia=False,
    )
    defaults.update(overrides)
    return SDFContext(**defaults)


def _high_risk_context(**overrides) -> SDFContext:
    """Entity processing 50M health records — high SDF potential."""
    defaults = dict(
        volume_of_personal_data_processed=50_000_000,
        sensitivity_of_personal_data=0.9,
        risk_to_rights_of_data_principals=0.85,
        risk_to_sovereignty_or_integrity=0.7,
        risk_to_electoral_democracy=0.6,
        risk_to_state_security=0.5,
        risk_to_public_order=0.4,
        notified_as_sdf_by_central_govt=False,
        has_appointed_dpo=True,
        has_appointed_data_auditor=True,
        conducts_periodic_dpia=True,
    )
    defaults.update(overrides)
    return SDFContext(**defaults)


# ═══════════════════════════════════════════════════════════════════════════
# Sec 10(1)(a) — volume + sensitivity
# ═══════════════════════════════════════════════════════════════════════════

class TestSec10_1_a:
    def test_high_volume_high_sensitivity_elevated(self):
        """Entity processing 50M health records → elevated volume + sensitivity concern."""
        ctx = _high_risk_context()
        result = check_sec_10_1_a(ctx)
        assert not result.compliant
        assert result.section == "Sec 10(1)(a)"
        assert "elevated" in result.reason

    def test_low_volume_low_sensitivity_not_elevated(self):
        """Small shop with 100 records → not an elevated concern."""
        ctx = _low_risk_context()
        result = check_sec_10_1_a(ctx)
        assert result.compliant
        assert "not an elevated concern" in result.reason

    def test_high_volume_low_sensitivity(self):
        """High volume but low sensitivity — volume signal dominates."""
        ctx = _low_risk_context(volume_of_personal_data_processed=8_000_000, sensitivity_of_personal_data=0.1)
        result = check_sec_10_1_a(ctx)
        # volume_signal = 8M/10M = 0.8, sensitivity = 0.1, combined = max(0.8, 0.1) = 0.8 >= 0.5
        assert not result.compliant

    def test_low_volume_high_sensitivity(self):
        """Low volume but high sensitivity — sensitivity dominates."""
        ctx = _low_risk_context(volume_of_personal_data_processed=100, sensitivity_of_personal_data=0.9)
        result = check_sec_10_1_a(ctx)
        # volume_signal = 100/10M ≈ 0.0, sensitivity = 0.9, combined = 0.9 >= 0.5
        assert not result.compliant

    def test_invalid_input(self):
        with pytest.raises(InvalidInputError, match="expected SDFContext"):
            check_sec_10_1_a({"not": "a context"})  # type: ignore[arg-type]


# ═══════════════════════════════════════════════════════════════════════════
# Sec 10(1)(b) — risk to rights of Data Principals
# ═══════════════════════════════════════════════════════════════════════════

class TestSec10_1_b:
    def test_high_risk_elevated(self):
        ctx = _low_risk_context(risk_to_rights_of_data_principals=0.8)
        result = check_sec_10_1_b(ctx)
        assert not result.compliant
        assert "elevated" in result.reason

    def test_low_risk_not_elevated(self):
        ctx = _low_risk_context(risk_to_rights_of_data_principals=0.2)
        result = check_sec_10_1_b(ctx)
        assert result.compliant
        assert "not an elevated concern" in result.reason

    def test_at_threshold_boundary(self):
        """Exactly at threshold — elevated."""
        ctx = _low_risk_context(risk_to_rights_of_data_principals=0.5)
        result = check_sec_10_1_b(ctx)
        assert not result.compliant

    def test_just_below_threshold(self):
        ctx = _low_risk_context(risk_to_rights_of_data_principals=0.49)
        result = check_sec_10_1_b(ctx)
        assert result.compliant

    def test_invalid_input(self):
        with pytest.raises(InvalidInputError):
            check_sec_10_1_b(None)  # type: ignore[arg-type]


# ═══════════════════════════════════════════════════════════════════════════
# Sec 10(1)(c) — sovereignty + integrity of India
# ═══════════════════════════════════════════════════════════════════════════

class TestSec10_1_c:
    def test_high_risk_elevated(self):
        ctx = _low_risk_context(risk_to_sovereignty_or_integrity=0.7)
        result = check_sec_10_1_c(ctx)
        assert not result.compliant

    def test_low_risk_not_elevated(self):
        ctx = _low_risk_context(risk_to_sovereignty_or_integrity=0.1)
        result = check_sec_10_1_c(ctx)
        assert result.compliant

    def test_invalid_input(self):
        with pytest.raises(InvalidInputError):
            check_sec_10_1_c("bad")  # type: ignore[arg-type]


# ═══════════════════════════════════════════════════════════════════════════
# Sec 10(1)(d) — electoral democracy
# ═══════════════════════════════════════════════════════════════════════════

class TestSec10_1_d:
    def test_high_risk_elevated(self):
        ctx = _low_risk_context(risk_to_electoral_democracy=0.8)
        result = check_sec_10_1_d(ctx)
        assert not result.compliant

    def test_low_risk_not_elevated(self):
        ctx = _low_risk_context(risk_to_electoral_democracy=0.05)
        result = check_sec_10_1_d(ctx)
        assert result.compliant

    def test_invalid_input(self):
        with pytest.raises(InvalidInputError):
            check_sec_10_1_d(42)  # type: ignore[arg-type]


# ═══════════════════════════════════════════════════════════════════════════
# Sec 10(1)(e) — security of the State
# ═══════════════════════════════════════════════════════════════════════════

class TestSec10_1_e:
    def test_high_risk_elevated(self):
        ctx = _low_risk_context(risk_to_state_security=0.9)
        result = check_sec_10_1_e(ctx)
        assert not result.compliant

    def test_low_risk_not_elevated(self):
        ctx = _low_risk_context(risk_to_state_security=0.0)
        result = check_sec_10_1_e(ctx)
        assert result.compliant

    def test_invalid_input(self):
        with pytest.raises(InvalidInputError):
            check_sec_10_1_e(3.14)  # type: ignore[arg-type]


# ═══════════════════════════════════════════════════════════════════════════
# Sec 10(1)(f) — public order
# ═══════════════════════════════════════════════════════════════════════════

class TestSec10_1_f:
    def test_high_risk_elevated(self):
        ctx = _low_risk_context(risk_to_public_order=0.75)
        result = check_sec_10_1_f(ctx)
        assert not result.compliant

    def test_low_risk_not_elevated(self):
        ctx = _low_risk_context(risk_to_public_order=0.0)
        result = check_sec_10_1_f(ctx)
        assert result.compliant

    def test_invalid_input(self):
        with pytest.raises(InvalidInputError):
            check_sec_10_1_f(b"bytes")  # type: ignore[arg-type]


# ═══════════════════════════════════════════════════════════════════════════
# assess_sdf_threshold — Sec 10(1) composite
# ═══════════════════════════════════════════════════════════════════════════

class TestAssessSdfThreshold:
    def test_50m_health_records_high_sdf_potential(self):
        """Entity processing 50M health records → high SDF potential (non-compliant)."""
        ctx = _high_risk_context()
        result = assess_sdf_threshold(ctx)
        assert not result.compliant
        assert "prepare SDF obligations" in result.reason
        assert len(result.sub_results) == 6  # one per 10(1)(a)-(f)

    def test_small_shop_100_records_not_sdf(self):
        """Small shop with 100 records → not SDF (compliant)."""
        ctx = _low_risk_context()
        result = assess_sdf_threshold(ctx)
        assert result.compliant
        assert "likely not SDF" in result.reason
        assert len(result.sub_results) == 6

    def test_notified_by_central_govt_short_circuit(self):
        """Central Govt notification short-circuits heuristic — always compliant."""
        ctx = _low_risk_context(notified_as_sdf_by_central_govt=True)
        result = assess_sdf_threshold(ctx)
        assert result.compliant
        assert "notified by Central Govt" in result.reason
        assert len(result.sub_results) == 6  # sub_results still populated

    def test_notified_overrides_high_heuristic(self):
        """Even with high-risk profile, govt notification makes it compliant."""
        ctx = _high_risk_context(notified_as_sdf_by_central_govt=True)
        result = assess_sdf_threshold(ctx)
        assert result.compliant
        assert "notified by Central Govt" in result.reason

    def test_moderate_profile_below_threshold(self):
        """Moderate scores across all factors but composite < 0.6."""
        ctx = SDFContext(
            volume_of_personal_data_processed=1_000_000,
            sensitivity_of_personal_data=0.3,
            risk_to_rights_of_data_principals=0.3,
            risk_to_sovereignty_or_integrity=0.2,
            risk_to_electoral_democracy=0.2,
            risk_to_state_security=0.2,
            risk_to_public_order=0.2,
        )
        result = assess_sdf_threshold(ctx)
        assert result.compliant

    def test_moderate_profile_at_threshold(self):
        """Composite exactly at 0.6 — non-compliant."""
        ctx = SDFContext(
            volume_of_personal_data_processed=10_000_000,
            sensitivity_of_personal_data=0.6,
            risk_to_rights_of_data_principals=0.6,
            risk_to_sovereignty_or_integrity=0.6,
            risk_to_electoral_democracy=0.6,
            risk_to_state_security=0.6,
            risk_to_public_order=0.6,
        )
        # volume_signal=1.0, composite = 0.2*1.0 + 0.2*0.6 + 0.2*0.6 + 0.1*0.6 + 0.1*0.6 + 0.1*0.6 + 0.1*0.6
        # = 0.2 + 0.12 + 0.12 + 0.06 + 0.06 + 0.06 + 0.06 = 0.68
        result = assess_sdf_threshold(ctx)
        assert not result.compliant

    def test_sub_results_include_all_six_factors(self):
        ctx = _high_risk_context()
        result = assess_sdf_threshold(ctx)
        sections = {r.section for r in result.sub_results}
        assert sections == {
            "Sec 10(1)(a)", "Sec 10(1)(b)", "Sec 10(1)(c)",
            "Sec 10(1)(d)", "Sec 10(1)(e)", "Sec 10(1)(f)",
        }

    def test_invalid_input(self):
        with pytest.raises(InvalidInputError, match="expected SDFContext"):
            assess_sdf_threshold("not an SDFContext")  # type: ignore[arg-type]


# ═══════════════════════════════════════════════════════════════════════════
# Sec 10(2)(a) — DPO appointment (with sub-clauses (i)-(iv))
# ═══════════════════════════════════════════════════════════════════════════

class TestSec10_2_a_DPO:
    def test_dpo_appointed_all_sub_checks_pass(self):
        """SDF with DPO appointed → all four sub-checks pass (proxy)."""
        ctx = _low_risk_context(has_appointed_dpo=True)
        result = check_sec_10_2_a_dpo(ctx)
        assert result.compliant
        assert result.section == "Sec 10(2)(a)"
        assert len(result.sub_results) == 4
        assert all(r.compliant for r in result.sub_results)

    def test_dpo_not_appointed_all_sub_checks_fail(self):
        """SDF without DPO → all four sub-checks fail."""
        ctx = _low_risk_context(has_appointed_dpo=False)
        result = check_sec_10_2_a_dpo(ctx)
        assert not result.compliant
        assert len(result.sub_results) == 4
        assert not any(r.compliant for r in result.sub_results)

    def test_sub_clause_sections_are_correct(self):
        ctx = _low_risk_context(has_appointed_dpo=True)
        result = check_sec_10_2_a_dpo(ctx)
        sections = {r.section for r in result.sub_results}
        assert sections == {
            "Sec 10(2)(a)(i)", "Sec 10(2)(a)(ii)",
            "Sec 10(2)(a)(iii)", "Sec 10(2)(a)(iv)",
        }

    def test_sub_clause_ii_dpo_based_in_india_failure_message(self):
        """When DPO not appointed, Sec 10(2)(a)(ii) shows India-based requirement."""
        ctx = _low_risk_context(has_appointed_dpo=False)
        result = check_sec_10_2_a_dpo(ctx)
        sub_ii = next(r for r in result.sub_results if r.section == "Sec 10(2)(a)(ii)")
        assert "based in India" in sub_ii.reason
        assert "150 crore" in sub_ii.reason

    def test_sub_clause_iii_board_accountability_message(self):
        ctx = _low_risk_context(has_appointed_dpo=False)
        result = check_sec_10_2_a_dpo(ctx)
        sub_iii = next(r for r in result.sub_results if r.section == "Sec 10(2)(a)(iii)")
        assert "Board of Directors" in sub_iii.reason

    def test_sub_clause_iv_grievance_contact_message(self):
        ctx = _low_risk_context(has_appointed_dpo=False)
        result = check_sec_10_2_a_dpo(ctx)
        sub_iv = next(r for r in result.sub_results if r.section == "Sec 10(2)(a)(iv)")
        assert "grievance redressal" in sub_iv.reason

    def test_invalid_input(self):
        with pytest.raises(InvalidInputError):
            check_sec_10_2_a_dpo(None)  # type: ignore[arg-type]


# ═══════════════════════════════════════════════════════════════════════════
# Sec 10(2)(b) — independent data auditor
# ═══════════════════════════════════════════════════════════════════════════

class TestSec10_2_b_Auditor:
    def test_auditor_appointed(self):
        ctx = _low_risk_context(has_appointed_data_auditor=True)
        result = check_sec_10_2_b_auditor(ctx)
        assert result.compliant
        assert "independent data auditor" in result.reason

    def test_auditor_not_appointed(self):
        """SDF without independent data auditor → fails Sec 10(2)(b)."""
        ctx = _low_risk_context(has_appointed_data_auditor=False)
        result = check_sec_10_2_b_auditor(ctx)
        assert not result.compliant
        assert "appoint an independent data auditor" in result.reason

    def test_invalid_input(self):
        with pytest.raises(InvalidInputError):
            check_sec_10_2_b_auditor(123)  # type: ignore[arg-type]


# ═══════════════════════════════════════════════════════════════════════════
# Sec 10(2)(c) — periodic DPIA + audit
# ═══════════════════════════════════════════════════════════════════════════

class TestSec10_2_c_DPIA:
    def test_dpia_conducted(self):
        ctx = _low_risk_context(conducts_periodic_dpia=True)
        result = check_sec_10_2_c_dpia(ctx)
        assert result.compliant
        assert len(result.sub_results) == 3

    def test_dpia_not_conducted(self):
        """SDF skips DPIA → fails Sec 10(2)(c)."""
        ctx = _low_risk_context(conducts_periodic_dpia=False)
        result = check_sec_10_2_c_dpia(ctx)
        assert not result.compliant
        assert "Data Protection Impact Assessment" in result.reason

    def test_sub_clauses_include_dpia_audit_and_other(self):
        ctx = _low_risk_context(conducts_periodic_dpia=True)
        result = check_sec_10_2_c_dpia(ctx)
        sections = {r.section for r in result.sub_results}
        assert sections == {"Sec 10(2)(c)(i)", "Sec 10(2)(c)(ii)", "Sec 10(2)(c)(iii)"}

    def test_other_measures_delegated_to_rules_always_compliant(self):
        """Sec 10(2)(c)(iii) delegates to DPDP Rules 2025 — currently always compliant."""
        ctx = _low_risk_context(conducts_periodic_dpia=False)
        result = check_sec_10_2_c_dpia(ctx)
        sub_iii = next(r for r in result.sub_results if r.section == "Sec 10(2)(c)(iii)")
        assert sub_iii.compliant
        assert "DPDP Rules 2025" in sub_iii.reason

    def test_invalid_input(self):
        with pytest.raises(InvalidInputError):
            check_sec_10_2_c_dpia([])  # type: ignore[arg-type]


# ═══════════════════════════════════════════════════════════════════════════
# Sec 10(2)(d) — other prescribed measures
# ═══════════════════════════════════════════════════════════════════════════

class TestSec10_2_d_OtherMeasures:
    def test_other_measures_compliant_by_default(self):
        """Without the proposed field, other measures default to compliant."""
        ctx = _low_risk_context()
        result = check_sec_10_2_d_other_measures(ctx)
        assert result.compliant
        assert "DPDP Rules 2025" in result.reason

    def test_invalid_input(self):
        with pytest.raises(InvalidInputError):
            check_sec_10_2_d_other_measures("nope")  # type: ignore[arg-type]


# ═══════════════════════════════════════════════════════════════════════════
# check_sdf_obligations — Sec 10(2) composite
# ═══════════════════════════════════════════════════════════════════════════

class TestCheckSdfObligations:
    def test_all_obligations_satisfied(self):
        """SDF with DPO, auditor, and DPIA → all obligations pass."""
        ctx = _low_risk_context(
            has_appointed_dpo=True,
            has_appointed_data_auditor=True,
            conducts_periodic_dpia=True,
        )
        result = check_sdf_obligations(ctx)
        assert result.compliant
        assert result.section == "Sec 10(2)"
        assert len(result.sub_results) == 4  # (a), (b), (c), (d)

    def test_dpo_missing_causes_failure(self):
        """SDF without DPO → obligations fail with DPO-related reason."""
        ctx = _low_risk_context(
            has_appointed_dpo=False,
            has_appointed_data_auditor=True,
            conducts_periodic_dpia=True,
        )
        result = check_sdf_obligations(ctx)
        assert not result.compliant
        assert "DPO" in result.reason

    def test_no_independent_auditor_causes_failure(self):
        """SDF without independent data auditor → fails Sec 10(2)(b)."""
        ctx = _low_risk_context(
            has_appointed_dpo=True,
            has_appointed_data_auditor=False,
            conducts_periodic_dpia=True,
        )
        result = check_sdf_obligations(ctx)
        assert not result.compliant
        assert "auditor" in result.reason.lower()

    def test_no_dpia_causes_failure(self):
        """SDF skips DPIA → fails Sec 10(2)(c)."""
        ctx = _low_risk_context(
            has_appointed_dpo=True,
            has_appointed_data_auditor=True,
            conducts_periodic_dpia=False,
        )
        result = check_sdf_obligations(ctx)
        assert not result.compliant
        assert "DPIA" in result.reason or "Impact Assessment" in result.reason

    def test_nothing_in_place_all_fail(self):
        """No DPO, no auditor, no DPIA → all obligations fail."""
        ctx = _low_risk_context(
            has_appointed_dpo=False,
            has_appointed_data_auditor=False,
            conducts_periodic_dpia=False,
        )
        result = check_sdf_obligations(ctx)
        assert not result.compliant
        # all four top-level sub_results should be non-compliant except (d) which defaults True
        non_compliant = [r for r in result.sub_results if not r.compliant]
        assert len(non_compliant) == 3

    def test_sub_results_sections_are_correct(self):
        ctx = _low_risk_context(
            has_appointed_dpo=True,
            has_appointed_data_auditor=True,
            conducts_periodic_dpia=True,
        )
        result = check_sdf_obligations(ctx)
        sections = {r.section for r in result.sub_results}
        assert sections == {"Sec 10(2)(a)", "Sec 10(2)(b)", "Sec 10(2)(c)", "Sec 10(2)(d)"}

    def test_invalid_input(self):
        with pytest.raises(InvalidInputError, match="expected SDFContext"):
            check_sdf_obligations(object())  # type: ignore[arg-type]


# ═══════════════════════════════════════════════════════════════════════════
# DPO in US scenario — documented limitation pending SDFContext field addition
# ═══════════════════════════════════════════════════════════════════════════

class TestDpoLocationLimitation:
    """Tests documenting the current proxy limitation.

    Once dpo_based_in_india is added to SDFContext (per proposed-fields
    comment block in sdf.py), these tests will validate the real location
    check. For now, has_appointed_dpo=True proxies all four sub-clauses
    including (ii) "based in India".
    """

    def test_dpo_location_proxy_current_behavior(self):
        """Currently, has_appointed_dpo=True passes Sec 10(2)(a)(ii) even though
        location is not independently verifiable. This test documents the proxy
        behaviour and should be updated when dpo_based_in_india is added to
        SDFContext."""
        ctx = _low_risk_context(has_appointed_dpo=True)
        result = check_sec_10_2_a_dpo(ctx)
        sub_ii = next(r for r in result.sub_results if r.section == "Sec 10(2)(a)(ii)")
        assert sub_ii.compliant  # proxy: has_appointed_dpo=True ⇒ all sub-clauses pass

    def test_dpo_in_us_would_fail_with_dedicated_field(self):
        """Documentation test: when dpo_based_in_india field is added to
        SDFContext, setting has_appointed_dpo=True + dpo_based_in_india=False
        should cause Sec 10(2)(a)(ii) to fail. This cannot be tested until
        the field is added to the frozen dataclass in dpdp/types.py."""
        # This test exists as a placeholder — the real assertion will be:
        #   ctx = SDFContext(..., has_appointed_dpo=True, dpo_based_in_india=False)
        #   result = check_sec_10_2_a_dpo(ctx)
        #   sub_ii = next(r for r in result.sub_results if r.section == "Sec 10(2)(a)(ii)")
        #   assert not sub_ii.compliant
        pass  # pending SDFContext field addition


# ═══════════════════════════════════════════════════════════════════════════
# Integration-style scenarios
# ═══════════════════════════════════════════════════════════════════════════

class TestEndToEndScenarios:
    def test_high_risk_entity_full_pipeline(self):
        """50M health records entity: threshold flags SDF concern, but obligations
        are met → threshold non-compliant, obligations compliant."""
        ctx = _high_risk_context(
            has_appointed_dpo=True,
            has_appointed_data_auditor=True,
            conducts_periodic_dpia=True,
        )
        threshold = assess_sdf_threshold(ctx)
        obligations = check_sdf_obligations(ctx)
        assert not threshold.compliant  # flagged as potential SDF
        assert obligations.compliant  # but obligations are met

    def test_small_shop_full_pipeline(self):
        """Small shop: threshold passes (not SDF concern), no obligations needed."""
        ctx = _low_risk_context()
        threshold = assess_sdf_threshold(ctx)
        assert threshold.compliant

    def test_notified_sdf_with_gaps(self):
        """Central-Govt-notified SDF that hasn't appointed DPO or auditor."""
        ctx = _low_risk_context(
            notified_as_sdf_by_central_govt=True,
            has_appointed_dpo=False,
            has_appointed_data_auditor=False,
            conducts_periodic_dpia=False,
        )
        threshold = assess_sdf_threshold(ctx)
        obligations = check_sdf_obligations(ctx)
        assert threshold.compliant  # notified → threshold passes
        assert not obligations.compliant  # but obligations are failing

    def test_compliance_result_is_falsy_when_non_compliant(self):
        ctx = _low_risk_context(has_appointed_dpo=False)
        result = check_sdf_obligations(ctx)
        assert not bool(result)
        assert not result

    def test_compliance_result_is_truthy_when_compliant(self):
        ctx = _low_risk_context(
            has_appointed_dpo=True,
            has_appointed_data_auditor=True,
            conducts_periodic_dpia=True,
        )
        result = check_sdf_obligations(ctx)
        assert bool(result)
        assert result

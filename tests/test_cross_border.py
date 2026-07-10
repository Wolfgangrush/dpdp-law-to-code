"""Tests for dpdp.cross_border — Sec 16 Cross-border transfer of personal data."""

from __future__ import annotations

import pytest

from dpdp.cross_border import (
    check_cross_border_transfer,
    check_sec_16_1_negative_list,
    check_sec_16_2_sectoral_law,
)
from dpdp.exceptions import InvalidInputError
from dpdp.types import ComplianceResult, CrossBorderTransfer

# ── helpers ────────────────────────────────────────────────────────────────


def _transfer(dest: str = "US", **kwargs: bool) -> CrossBorderTransfer:
    """Build a CrossBorderTransfer with all restriction flags defaulting False."""
    defaults: dict[str, bool | str] = {
        "destination_country_iso": dest,
        "sectoral_law_restriction_applies": False,
        "central_govt_has_notified_restriction": False,
        "sub_processor_contract_in_place": False,
    }
    defaults.update(kwargs)
    return CrossBorderTransfer(**defaults)  # type: ignore[arg-type]


# ── Sec 16(1) — Negative List ─────────────────────────────────────────────


class TestSec16_1_NegativeList:
    def test_pass_default_permit(self):
        """Transfer to US — no Central Govt notification, no country on negative list."""
        result = check_sec_16_1_negative_list(_transfer())
        assert result.compliant
        assert result.section == "Sec 16(1)"
        assert "not on" in result.reason.lower()

    def test_fail_central_govt_notified_restriction(self):
        """Central Govt has notified a restriction for the destination country."""
        result = check_sec_16_1_negative_list(
            _transfer(dest="CN", central_govt_has_notified_restriction=True)
        )
        assert not result.compliant
        assert result.section == "Sec 16(1)"
        assert "restricted" in result.reason.lower()
        assert "CN" in result.reason
        assert result.citation == "DPDP Act 2023, Sec 16(1)"

    def test_fail_country_in_negative_list(self, monkeypatch):
        """Destination country is on the Central Govt notified negative list."""
        monkeypatch.setattr(
            "dpdp.cross_border._NOTIFIED_RESTRICTED_COUNTRIES",
            frozenset({"CN", "PK"}),
        )
        result = check_sec_16_1_negative_list(_transfer(dest="PK"))
        assert not result.compliant
        assert result.section == "Sec 16(1)"
        assert "restricted" in result.reason.lower()
        assert "PK" in result.reason

    def test_invalid_input_raises(self):
        with pytest.raises(InvalidInputError, match="expected CrossBorderTransfer"):
            check_sec_16_1_negative_list(None)  # type: ignore[arg-type]


# ── Sec 16(2) — Sectoral Law Preservation ─────────────────────────────────


class TestSec16_2_SectoralLaw:
    def test_pass_no_sectoral_restriction(self):
        """No sectoral-law restriction applies — Sec 16(2) not triggered."""
        result = check_sec_16_2_sectoral_law(_transfer())
        assert result.compliant
        assert result.section == "Sec 16(2)"
        assert "does not apply" in result.reason.lower()

    def test_fail_sectoral_restriction_applies(self):
        """RBI circular restricts cross-border transfer of banking customer data."""
        result = check_sec_16_2_sectoral_law(
            _transfer(sectoral_law_restriction_applies=True)
        )
        assert not result.compliant
        assert result.section == "Sec 16(2)"
        assert "higher protection" in result.reason.lower()
        assert "RBI" in result.reason
        assert result.citation == "DPDP Act 2023, Sec 16(2)"

    def test_invalid_input_raises(self):
        with pytest.raises(InvalidInputError, match="expected CrossBorderTransfer"):
            check_sec_16_2_sectoral_law(None)  # type: ignore[arg-type]


# ── Master Aggregator — check_cross_border_transfer ───────────────────────


class TestCrossBorderTransferMaster:
    def test_pass_no_restrictions(self):
        """Transfer to US — no Central Govt negative list, no sectoral restriction."""
        result = check_cross_border_transfer(_transfer())
        assert result.compliant
        assert result.section == "Sec 16"
        assert "permissible" in result.reason.lower()
        assert len(result.sub_results) == 2
        assert all(r.compliant for r in result.sub_results)

    def test_fail_negative_list_blocks(self):
        """Central Govt notifies restriction — Sec 16(1) blocks, Sec 16(2) passes."""
        result = check_cross_border_transfer(
            _transfer(dest="CN", central_govt_has_notified_restriction=True)
        )
        assert not result.compliant
        assert result.section == "Sec 16"
        assert "Sec 16(1)" in result.reason
        assert len(result.sub_results) == 2
        # Sec 16(2) sub-result should be compliant, Sec 16(1) not
        assert result.sub_results[1].compliant  # 16(2)
        assert not result.sub_results[0].compliant  # 16(1)

    def test_fail_sectoral_law_trumps(self):
        """Sectoral law (RBI) restricts transfer even though country not on negative list."""
        result = check_cross_border_transfer(
            _transfer(dest="US", sectoral_law_restriction_applies=True)
        )
        assert not result.compliant
        assert result.section == "Sec 16"
        assert "sectoral law" in result.reason.lower()
        assert "trumps" in result.reason.lower()
        assert len(result.sub_results) == 2
        # Sec 16(1) sub-result should be compliant, Sec 16(2) not
        assert result.sub_results[0].compliant  # 16(1)
        assert not result.sub_results[1].compliant  # 16(2)

    def test_fail_both_restrictions(self):
        """Both negative list AND sectoral restriction apply — Sec 16(2) trumps message."""
        result = check_cross_border_transfer(
            _transfer(
                dest="CN",
                central_govt_has_notified_restriction=True,
                sectoral_law_restriction_applies=True,
            )
        )
        assert not result.compliant
        assert result.section == "Sec 16"
        assert "sectoral law" in result.reason.lower()
        assert "trumps" in result.reason.lower()
        assert len(result.sub_results) == 2
        assert not result.sub_results[0].compliant  # 16(1)
        assert not result.sub_results[1].compliant  # 16(2)

    def test_sub_results_structure(self):
        """Master result includes both sub-checkers with correct section fields."""
        result = check_cross_border_transfer(_transfer())
        sections = {r.section for r in result.sub_results}
        assert sections == {"Sec 16(1)", "Sec 16(2)"}
        assert all(isinstance(r, ComplianceResult) for r in result.sub_results)

    def test_invalid_input_raises(self):
        with pytest.raises(InvalidInputError, match="expected CrossBorderTransfer"):
            check_cross_border_transfer(None)  # type: ignore[arg-type]

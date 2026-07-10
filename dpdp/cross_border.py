"""Sec 16 — Cross-border transfer of personal data.

Citation: DPDP Act 2023, Sec 16.
Last updated: 2026-05-23.

Sec 16(1) — Central Govt may, by notification, restrict the transfer of
personal data by a Data Fiduciary to such country or territory outside
India as may be notified. (NEGATIVE LIST mechanism.)

Sec 16(2) — Nothing in 16(1) shall restrict the applicability of any law
in force in India that provides for a higher degree of protection /
restriction. (SECTORAL LAW PRESERVATION — RBI / SEBI / IRDAI / TRAI /
MoH&FW.)

Default position: general permission for transfer of personal data outside
India, subject to (a) any restriction notified by Central Govt under
Sec 16(1), and (b) any sectoral law that imposes higher protection.

This module is not legal advice. It encodes a developer-friendly reading of
DPDP Act 2023 Sec 16 for compliance harness purposes. Consult qualified
counsel before relying on outputs for regulatory or contentious matters.
"""

from __future__ import annotations

from dpdp.exceptions import InvalidInputError
from dpdp.types import ComplianceResult, CrossBorderTransfer

# v0.1: no Central Govt negative-list notification published as of 2026-05-23.
# This set is the ledger; update when MeitY publishes.
_NOTIFIED_RESTRICTED_COUNTRIES: frozenset[str] = frozenset()


def check_sec_16_1_negative_list(transfer: CrossBorderTransfer) -> ComplianceResult:
    """Check Central Govt negative-list restriction under Sec 16(1)."""
    if not isinstance(transfer, CrossBorderTransfer):
        raise InvalidInputError("expected CrossBorderTransfer", section="Sec 16(1)")

    restricted = (
        transfer.central_govt_has_notified_restriction
        or transfer.destination_country_iso in _NOTIFIED_RESTRICTED_COUNTRIES
    )

    if restricted:
        return ComplianceResult(
            compliant=False,
            section="Sec 16(1)",
            reason=(
                f"transfer to {transfer.destination_country_iso} restricted by Central Govt"
                " notification under Sec 16(1)"
            ),
            citation="DPDP Act 2023, Sec 16(1)",
        )

    return ComplianceResult(
        compliant=True,
        section="Sec 16(1)",
        reason=(
            f"transfer to {transfer.destination_country_iso} not on Central Govt"
            " negative list — Sec 16(1) does not bar transfer"
        ),
        citation="DPDP Act 2023, Sec 16(1)",
    )


def check_sec_16_2_sectoral_law(transfer: CrossBorderTransfer) -> ComplianceResult:
    """Check sectoral-law preservation under Sec 16(2)."""
    if not isinstance(transfer, CrossBorderTransfer):
        raise InvalidInputError("expected CrossBorderTransfer", section="Sec 16(2)")

    if transfer.sectoral_law_restriction_applies:
        return ComplianceResult(
            compliant=False,
            section="Sec 16(2)",
            reason=(
                "sectoral law (e.g. RBI / SEBI / IRDAI / TRAI / MoH&FW)"
                " imposes higher protection — Sec 16(2) preserves such restriction"
            ),
            citation="DPDP Act 2023, Sec 16(2)",
        )

    return ComplianceResult(
        compliant=True,
        section="Sec 16(2)",
        reason=("no sectoral-law restriction asserted — Sec 16(2) does not apply"),
        citation="DPDP Act 2023, Sec 16(2)",
    )


def check_cross_border_transfer(transfer: CrossBorderTransfer) -> ComplianceResult:
    """Validate a proposed cross-border transfer against Sec 16.

    Per DPDP Act 2023, Sec 16, the default position is general permission for
    transfer of personal data outside India, subject to (a) any restriction
    notified by the Central Govt under Sec 16(1), and (b) any sectoral law
    that imposes higher protection under Sec 16(2).
    """
    if not isinstance(transfer, CrossBorderTransfer):
        raise InvalidInputError("expected CrossBorderTransfer", section="Sec 16")

    r_16_2 = check_sec_16_2_sectoral_law(transfer)
    r_16_1 = check_sec_16_1_negative_list(transfer)

    # Sec 16(2) sectoral-law restriction trumps Sec 16(1) — even if country is
    # not on the negative list, a higher-protection sectoral law blocks transfer.
    if not r_16_2.compliant:
        return ComplianceResult(
            compliant=False,
            section="Sec 16",
            reason=(
                f"transfer to {transfer.destination_country_iso} barred —"
                " sectoral law imposes higher protection (Sec 16(2) trumps)"
            ),
            citation="DPDP Act 2023, Sec 16",
            sub_results=[r_16_1, r_16_2],
        )

    if not r_16_1.compliant:
        return ComplianceResult(
            compliant=False,
            section="Sec 16",
            reason=(
                f"transfer to {transfer.destination_country_iso} restricted by"
                " Central Govt notification under Sec 16(1)"
            ),
            citation="DPDP Act 2023, Sec 16",
            sub_results=[r_16_1, r_16_2],
        )

    return ComplianceResult(
        compliant=True,
        section="Sec 16",
        reason=(
            f"transfer to {transfer.destination_country_iso} permissible —"
            " no Central Govt restriction notified + no higher sectoral law"
            " restriction asserted"
        ),
        citation="DPDP Act 2023, Sec 16",
        sub_results=[r_16_1, r_16_2],
    )

"""Example — audit a cookie / consent banner against DPDP Sec 6.

Run:
    python examples/consent_banner_check.py
"""

from __future__ import annotations

from dpdp.consent import check_consent
from dpdp.types import ConsentRecord


def main() -> None:
    # A typical "Accept All" pre-checked banner that bundles marketing + analytics
    # with strictly-necessary cookies — common pre-DPDP design.
    typical_pre_dpdp_banner = ConsentRecord(
        is_free=False,
        is_specific=False,
        is_informed=False,
        is_unconditional=False,
        is_unambiguous=False,
        has_clear_affirmative_action=False,
        is_limited_to_specified_purpose=False,
        is_withdrawable_easily=False,
        is_pre_checked=True,
        is_bundled_with_unrelated_terms=True,
    )

    print("Scenario A — typical 'Accept All' pre-checked bundled banner:")
    print(check_consent(typical_pre_dpdp_banner))
    print()

    # A DPDP-compliant banner: per-purpose granular toggles, default OFF, easy
    # withdraw link in footer, Sec 5 notice linked alongside.
    dpdp_compliant_banner = ConsentRecord(
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
    )

    print("Scenario B — DPDP-compliant granular banner:")
    print(check_consent(dpdp_compliant_banner))


if __name__ == "__main__":
    main()

"""Verbatim DPDP Act 2023 section text — machine-addressable lookup.

Each section text is the official MeitY-published text. Source: meity.gov.in.
"""

from __future__ import annotations

# Key = canonical section cite (e.g. "Sec 6(1)"). Value = verbatim text.
ACT_TEXT: dict[str, str] = {
    # "Sec 1": "...",
    # "Sec 2": "...",
    # ... populated Day 0 morning
}


def get_section(cite: str) -> str:
    """Return the verbatim text of a DPDP Act 2023 section.

    Per DPDP Act 2023; cite format e.g. "Sec 6(1)" or "Sec 9".
    """
    if cite not in ACT_TEXT:
        return f"[TEXT NOT YET ENCODED — {cite}]"
    return ACT_TEXT[cite]

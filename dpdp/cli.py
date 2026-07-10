"""Command-line interface for dpdp-law-to-code.

Usage:
    dpdp-check --section 6 --input consent.json
    dpdp-check --list-sections
    dpdp-check --version
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Callable

from dpdp import __version__
from dpdp.children import check_child_processing
from dpdp.consent import check_consent
from dpdp.cross_border import check_cross_border_transfer
from dpdp.duties import check_data_principal_duty
from dpdp.exceptions import DPDPViolationError
from dpdp.fiduciary import check_breach_notification
from dpdp.legitimate import check_legitimate_use
from dpdp.notice import check_notice
from dpdp.rights import check_rights_response
from dpdp.sdf import assess_sdf_threshold, check_sdf_obligations
from dpdp.types import (
    BreachRecord,
    ChildRecord,
    ComplianceResult,
    ConsentRecord,
    CrossBorderTransfer,
    DataPrincipalDuty,
    LegitimateUseCase,
    LegitimateUseRecord,
    NoticeRecord,
    RightsRequest,
    RightType,
    SDFContext,
)


SECTION_REGISTRY: dict[str, tuple[Callable[..., ComplianceResult], type, str]] = {
    "5": (check_notice, NoticeRecord, "Notice"),
    "6": (check_consent, ConsentRecord, "Consent"),
    "7": (check_legitimate_use, LegitimateUseRecord, "Legitimate Uses"),
    "8": (
        check_breach_notification,
        BreachRecord,
        "Data Fiduciary obligations — breach notification",
    ),
    "9": (check_child_processing, ChildRecord, "Children"),
    "10": (check_sdf_obligations, SDFContext, "Significant Data Fiduciary"),
    "10-threshold": (assess_sdf_threshold, SDFContext, "SDF threshold assessment"),
    "11-14": (check_rights_response, RightsRequest, "Data Principal Rights"),
    "15": (check_data_principal_duty, DataPrincipalDuty, "Data Principal Duties"),
    "16": (check_cross_border_transfer, CrossBorderTransfer, "Cross-border transfer"),
}


def _hydrate(record_type: type, data: dict[str, Any]) -> Any:
    """Construct a dataclass from a JSON dict, resolving enum strings."""
    if record_type is LegitimateUseRecord and "asserted_case" in data:
        data = {**data, "asserted_case": LegitimateUseCase(data["asserted_case"])}
    if record_type is RightsRequest and "right" in data:
        data = {**data, "right": RightType(data["right"])}
    return record_type(**data)


def _serialize(result: ComplianceResult) -> dict[str, Any]:
    out = asdict(result) if is_dataclass(result) else {}
    return out


def cmd_check(args: argparse.Namespace) -> int:
    if args.section not in SECTION_REGISTRY:
        print(
            f"error: unknown section '{args.section}'. --list-sections for options.",
            file=sys.stderr,
        )
        return 2

    fn, record_type, _name = SECTION_REGISTRY[args.section]

    try:
        raw = json.loads(Path(args.input).read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: cannot read input {args.input}: {exc}", file=sys.stderr)
        return 2

    try:
        record = _hydrate(record_type, raw)
        result = fn(record)
    except DPDPViolationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 3

    if args.json:
        print(json.dumps(_serialize(result), indent=2, default=str))
    else:
        _print_human(result)
    return 0 if result.compliant else 1


def _print_human(result: ComplianceResult, indent: int = 0) -> None:
    prefix = "  " * indent
    badge = "✓" if result.compliant else "✗"
    print(f"{prefix}{badge} [{result.section}] {result.reason}")
    print(f"{prefix}  cite: {result.citation}")
    for sub in result.sub_results:
        _print_human(sub, indent + 1)


def cmd_list(args: argparse.Namespace) -> int:
    print("Encoded DPDP sections:")
    for key, (_, _, name) in SECTION_REGISTRY.items():
        print(f"  --section {key:<12}  {name}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="dpdp-check",
        description="DPDP Act 2023 compliance checker (v0.1). Not legal advice.",
    )
    parser.add_argument(
        "--version", action="version", version=f"dpdp-check {__version__}"
    )
    parser.add_argument("--list-sections", dest="list_sections", action="store_true")
    parser.add_argument(
        "--section", help="Section key (e.g. 6, 9, 16). See --list-sections."
    )
    parser.add_argument(
        "--input", help="Path to JSON input matching the section's record schema."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON output instead of human-readable.",
    )
    args = parser.parse_args()

    if args.list_sections:
        return cmd_list(args)

    if not args.section or not args.input:
        parser.print_help(sys.stderr)
        return 2

    return cmd_check(args)


if __name__ == "__main__":
    raise SystemExit(main())

"""dpdp-law-to-code — India's Digital Personal Data Protection Act 2023 as runnable Python.

Not legal advice. See LICENSE and README.md.
"""

from __future__ import annotations

__version__ = "0.1.0"

from dpdp.exceptions import DPDPViolationError
from dpdp.types import (
    BreachRecord,
    ChildRecord,
    ComplianceResult,
    ConsentRecord,
    CrossBorderTransfer,
    DataPrincipalDuty,
    LegitimateUseRecord,
    NoticeRecord,
    RightsRequest,
    SDFContext,
)

__all__ = [
    "__version__",
    "ComplianceResult",
    "DPDPViolationError",
    "ConsentRecord",
    "NoticeRecord",
    "LegitimateUseRecord",
    "ChildRecord",
    "SDFContext",
    "BreachRecord",
    "RightsRequest",
    "DataPrincipalDuty",
    "CrossBorderTransfer",
]

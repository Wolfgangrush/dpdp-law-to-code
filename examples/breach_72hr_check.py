"""Example — verify breach-notification timeliness against DPDP Sec 8(6).

Run:
    python examples/breach_72hr_check.py
"""

from __future__ import annotations

import time

from dpdp.fiduciary import check_breach_notification
from dpdp.types import BreachRecord


def main() -> None:
    now = int(time.time())

    # Scenario A — Data Fiduciary detected breach but waited 5 days to notify.
    late = BreachRecord(
        detected_at_unix=now - 5 * 86400,
        notified_board_at_unix=now,
        notified_affected_principals_at_unix=now,
        affected_principal_count=12_400,
        breach_description="auth token leak via misconfigured S3 bucket",
        contains_sensitive_categories=False,
    )
    print("Scenario A — 5-day delayed notification:")
    print(check_breach_notification(late))
    print()

    # Scenario B — notified Board within 18hrs, principals within 36hrs.
    timely = BreachRecord(
        detected_at_unix=now - 36 * 3600,
        notified_board_at_unix=now - 18 * 3600,
        notified_affected_principals_at_unix=now,
        affected_principal_count=12_400,
        breach_description="auth token leak via misconfigured S3 bucket",
        contains_sensitive_categories=False,
    )
    print("Scenario B — within heuristic 72hr window:")
    print(check_breach_notification(timely))


if __name__ == "__main__":
    main()

"""Shared types for DPDP compliance checks.

Every checker returns ComplianceResult. Input dataclasses model the
fact-patterns that a Data Fiduciary asserts. Keep these stdlib-only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


@dataclass(frozen=True)
class ComplianceResult:
    """Return shape for every check_* function in the dpdp package.

    Per DPDP Act 2023; `section` is the human-readable cite (e.g. "Sec 6(1)").
    `citation` is the canonical form for machine indexing.
    """

    compliant: bool
    section: str
    reason: str
    citation: str
    sub_results: list[ComplianceResult] = field(default_factory=list)

    def __bool__(self) -> bool:
        return self.compliant


# ─── Sec 5 — Notice ────────────────────────────────────────────────────
@dataclass(frozen=True)
class LegacyNoticeRecord:
    """Legacy-data notice under DPDP Act 2023, Sec 5(2).

    For personal data collected BEFORE the Act's commencement. Data
    Fiduciary must give fresh notice "as soon as reasonably practicable"
    to enable the Data Principal to exercise rights under Sec 6(4) and
    Sec 13.
    """

    describes_personal_data: bool
    describes_purpose: bool
    describes_rights_exercise_method: bool
    describes_complaint_method_to_board: bool
    available_in_english_or_eighth_schedule_language: bool
    given_after_act_commencement_date: bool
    given_within_reasonable_time: bool


@dataclass(frozen=True)
class NoticeRecord:
    """Notice given by a Data Fiduciary before / at the time of seeking consent.

    Per DPDP Act 2023, Sec 5(1) — notice must contain enumerated items.
    """

    describes_personal_data: bool
    describes_purpose: bool
    describes_rights_exercise_method: bool
    describes_complaint_method_to_board: bool
    available_in_english_or_eighth_schedule_language: bool
    is_given_before_or_with_consent_request: bool


# ─── Sec 6 — Consent ───────────────────────────────────────────────────
@dataclass(frozen=True)
class ConsentRecord:
    """Consent obtained from a Data Principal.

    Per DPDP Act 2023, Sec 6(1) — F-S-I-U-U + clear affirmative action.
    Sec 6(4) — withdrawal must be as easy as giving.
    """

    is_free: bool
    is_specific: bool
    is_informed: bool
    is_unconditional: bool
    is_unambiguous: bool
    has_clear_affirmative_action: bool
    is_limited_to_specified_purpose: bool
    is_withdrawable_easily: bool
    is_pre_checked: bool = False
    is_bundled_with_unrelated_terms: bool = False
    # Sec 6(2) — invalidity of infringing parts of consent
    has_infringing_provision: bool = False
    # Sec 6(3) — clear/plain language + Eighth Schedule option + DPO contact
    request_in_clear_plain_language: bool = False
    has_eighth_schedule_language_option: bool = False
    dpo_contact_provided: bool = False


# ─── Sec 7 — Legitimate Uses ───────────────────────────────────────────
class LegitimateUseCase(str, Enum):
    """The 9 enumerated legitimate uses under DPDP Act 2023, Sec 7 (gazetted)."""

    VOLUNTARY_PROVISION_FOR_SPECIFIED_PURPOSE = "sec_7_a"  # Sec 7(a)
    STATE_SUBSIDY_BENEFIT_SERVICE_LICENSE = "sec_7_b"  # Sec 7(b)
    STATE_FUNCTION_UNDER_LAW = "sec_7_c"  # Sec 7(c)
    LEGAL_DISCLOSURE_TO_STATE = "sec_7_d"  # Sec 7(d)
    COURT_JUDGMENT_COMPLIANCE = "sec_7_e"  # Sec 7(e)
    MEDICAL_EMERGENCY = "sec_7_f"  # Sec 7(f) — renumbered from sec_7_d in gazette
    EPIDEMIC_PUBLIC_HEALTH_EMERGENCY = "sec_7_g"  # Sec 7(g) — renumbered from sec_7_e
    DISASTER_OR_BREAKDOWN_OF_PUBLIC_ORDER = "sec_7_h"  # Sec 7(h) — renumbered from sec_7_f
    EMPLOYMENT_PURPOSES = "sec_7_i"  # Sec 7(i) — renumbered from sec_7_g


@dataclass(frozen=True)
class LegitimateUseRecord:
    """A processing activity claimed under one of the 7 legitimate uses."""

    asserted_case: LegitimateUseCase
    purpose_description: str
    is_personal_data_voluntarily_provided: bool = False
    is_state_function: bool = False
    is_employment_related: bool = False
    threatens_life_or_health: bool = False
    has_other_lawful_basis: bool = True


# ─── Sec 8 — Data Fiduciary obligations ────────────────────────────────
@dataclass(frozen=True)
class ErasureContext:
    """Context for Sec 8(7) erasure obligations.

    Per DPDP Act 2023, Sec 8(7)(a) — Data Fiduciary erases on consent
    withdrawal or when specified purpose is served, whichever earlier,
    unless retention required by law. Sec 8(7)(b) — cascade to Processor.
    """

    consent_withdrawn: bool
    purpose_served: bool
    retention_required_by_law: bool
    fiduciary_erased: bool
    processor_erased: bool


@dataclass(frozen=True)
class BreachRecord:
    """A personal-data breach record.

    Per DPDP Act 2023, Sec 8(6) + Draft Rules 2025 — notify Board + affected
    Data Principals "without delay".
    """

    detected_at_unix: int
    notified_board_at_unix: int | None
    notified_affected_principals_at_unix: int | None
    affected_principal_count: int
    breach_description: str
    contains_sensitive_categories: bool = False


# ─── Sec 9 — Children ──────────────────────────────────────────────────
@dataclass(frozen=True)
class ChildRecord:
    """Processing of a child's personal data (under 18 per DPDP definition).

    Per DPDP Act 2023, Sec 9 — verifiable parental consent + no tracking +
    no targeted ads. Sec 9(4)/9(5) — Central Government exemption mechanisms.
    """

    data_principal_age: int
    has_verifiable_parental_consent: bool
    is_tracking_behavior: bool
    is_targeted_advertising: bool
    is_likely_to_cause_detrimental_effect: bool
    is_class_exempted_by_notification: bool = False


# ─── Sec 10 — Significant Data Fiduciary ───────────────────────────────
@dataclass(frozen=True)
class SDFContext:
    """Context for assessing whether an entity is a Significant Data Fiduciary.

    Per DPDP Act 2023, Sec 10(1) — Central Govt notifies SDFs basing on:
    volume / sensitivity / risk / potential impact on sovereignty / electoral
    democracy / security / public order.
    """

    volume_of_personal_data_processed: int
    sensitivity_of_personal_data: float  # 0..1 heuristic
    risk_to_rights_of_data_principals: float  # 0..1 heuristic
    risk_to_sovereignty_or_integrity: float  # 0..1 heuristic
    risk_to_electoral_democracy: float  # 0..1 heuristic
    risk_to_state_security: float  # 0..1 heuristic
    risk_to_public_order: float  # 0..1 heuristic
    notified_as_sdf_by_central_govt: bool = False
    has_appointed_dpo: bool = False
    has_appointed_data_auditor: bool = False
    conducts_periodic_dpia: bool = False


# ─── Sec 11–14 — Data Principal Rights ─────────────────────────────────
class RightType(str, Enum):
    ACCESS_AND_INFORMATION = "sec_11"  # Sec 11
    CORRECTION_AND_ERASURE = "sec_12"  # Sec 12
    GRIEVANCE_REDRESSAL = "sec_13"  # Sec 13
    NOMINATION = "sec_14"  # Sec 14


@dataclass(frozen=True)
class RightsRequest:
    """A Data Principal exercising one of the rights under Sec 11-14."""

    right: RightType
    received_at_unix: int
    responded_at_unix: int | None
    grievance_resolution_period_days: int = 30


# ─── Sec 15 — Data Principal Duties ────────────────────────────────────
@dataclass(frozen=True)
class DataPrincipalDuty:
    """Conduct of a Data Principal that may attract Sec 15 + Schedule penalty.

    Per DPDP Act 2023, Sec 15 — false particulars / impersonation /
    suppression / frivolous grievance / false complaint.
    """

    submitted_false_particulars: bool
    impersonated_another_person: bool
    suppressed_material_information: bool
    filed_frivolous_grievance: bool
    filed_false_complaint: bool


# ─── Sec 16 — Cross-Border Transfer ────────────────────────────────────
@dataclass(frozen=True)
class CrossBorderTransfer:
    """A proposed transfer of personal data outside India.

    Per DPDP Act 2023, Sec 16 — Central Govt may, by notification, restrict
    transfer to certain countries / territories outside India. Default is
    "general permission" subject to such restrictions.
    """

    destination_country_iso: str
    sectoral_law_restriction_applies: bool = False
    central_govt_has_notified_restriction: bool = False
    sub_processor_contract_in_place: bool = False

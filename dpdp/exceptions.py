"""DPDP-specific exceptions."""

from __future__ import annotations


class DPDPViolationError(Exception):
    """Raised when input cannot be validated against a DPDP obligation.

    Carries the section citation that triggered the failure.
    """

    def __init__(self, message: str, section: str) -> None:
        super().__init__(message)
        self.section = section

    def __str__(self) -> str:
        return f"[{self.section}] {super().__str__()}"


class InvalidInputError(DPDPViolationError):
    """Input shape is malformed (missing required field, wrong type, etc.)."""


class StatuteNotEncodedError(DPDPViolationError):
    """Section is in scope but not yet encoded in v0.1."""

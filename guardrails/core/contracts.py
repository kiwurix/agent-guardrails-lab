from dataclasses import dataclass
from typing import Any
from authentication import AuthenticatedUser
from .enums import GuardrailAction


@dataclass(frozen=True)
class GuardrailContext:
    authenticated_user: AuthenticatedUser
    ticket_id: int
    tool_name: str
    tool_args: dict[str, Any]
    tool_metadata: dict[str, Any]


@dataclass(frozen=True)
class GuardrailDecision:
    guardrail_name: str
    action: GuardrailAction
    reason: str | None = None

    def __post_init__(self):
        if self.action == GuardrailAction.BLOCK and self.reason is None:
            raise ValueError("Reason is required when action is block")


@dataclass(frozen=True)
class AggregatedGuardrailDecision:
    action: GuardrailAction
    decisions: tuple[GuardrailDecision, ...]

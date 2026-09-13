from typing import Any
from pydantic import BaseModel, ConfigDict, model_validator
from authentication.identity import AuthenticatedUser
from .enums import GuardrailAction


class GuardrailContext(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True)

    authenticated_user: AuthenticatedUser
    ticket_id: int
    tool_name: str
    tool_args: dict[str, Any]
    tool_metadata: dict[str, Any]


class GuardrailDecision(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True)

    guardrail_name: str
    action: GuardrailAction
    reason: str|None = None

    @model_validator(mode="after")
    def validate_reason(self):
        if self.action == GuardrailAction.BLOCK and self.reason is None:
            raise ValueError("Reason is required when action is block")

        return self

class AggregatedGuardrailDecision(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True)

    action: GuardrailAction
    decisions: tuple[GuardrailDecision, ...]


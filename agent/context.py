from dataclasses import dataclass
from authentication import AuthenticatedUser
from guardrails.runtime import GuardrailManager
from sqlalchemy.orm import Session


@dataclass
class AgentContext:
    authenticated_user: AuthenticatedUser
    guardrail_manager: GuardrailManager
    session: Session
    ticket_id: int

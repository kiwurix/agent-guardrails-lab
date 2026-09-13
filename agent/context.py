from dataclasses import dataclass
from authentication.identity import AuthenticatedUser
from guardrails.runtime.manager import GuardrailManager
from sqlalchemy.orm import Session


@dataclass
class AgentContext:
    authenticated_user: AuthenticatedUser
    guardrail_manager: GuardrailManager
    session: Session
    ticket_id: int
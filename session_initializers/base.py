from abc import ABC, abstractmethod
from dataclasses import dataclass
from data.database import Ticket, User
from langchain_core.messages import AnyMessage, SystemMessage, AIMessage
from sqlalchemy.orm import Session
from agent.context import AgentContext
from agent.state import AgentState
from authentication.identity import AuthenticatedUser
from guardrails.runtime.manager import GuardrailManager
from guardrails.runtime.registry import GuardrailRegistration


@dataclass
class InitializedSession:
    state: AgentState
    context: AgentContext


class BaseSessionBuilder(ABC):
    def __init__(self, session: Session):
        self.session = session
        self.messages: list[AnyMessage] = []
        self.authenticated_user: AuthenticatedUser | None = None
        self.ticket: Ticket | None = None

    @abstractmethod
    def _get_messages(self) -> None:
        pass

    @abstractmethod
    def _authenticate_user(self) -> None:
        pass

    @abstractmethod
    def _get_ticket(self) -> None:
        pass

    @abstractmethod
    def _create_user(self) -> User:
        pass

    @abstractmethod
    def _create_ticket(self) -> Ticket:
        pass

    @abstractmethod
    def _append_human_message(self):
        pass

    @abstractmethod
    def _get_guardrail_registrations(self) -> list[GuardrailRegistration]:
        pass

    def _check_last_message(self):
        if self.messages is None:
            raise RuntimeError

        if len(self.messages) == 0 or isinstance(self.messages[-1], AIMessage):
            self._append_human_message()


    def initialize(self) -> InitializedSession:
        self._authenticate_user()
        self._get_ticket()
        registrations = self._get_guardrail_registrations()
        self._get_messages()
        self._check_last_message()

        if self.messages is None or self.authenticated_user is None or self.ticket is None:
            raise RuntimeError("Session initialization is incomplete")

        self.messages.insert(0, SystemMessage(content=self.get_ticket_prompt()))

        state = AgentState(messages=self.messages)
        context = AgentContext(
            authenticated_user=self.authenticated_user,
            guardrail_manager=GuardrailManager(registrations),
            session=self.session,
            ticket_id=self.ticket.id,
        )

        return InitializedSession(state=state, context=context)


    def get_ticket_prompt(self):
        if self.ticket is None:
            raise RuntimeError

        return f"Now, you are working with this ticket:\n {self.ticket.to_dict()}"

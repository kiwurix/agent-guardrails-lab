from abc import ABC, abstractmethod
from data.database import Ticket
from langchain_core.messages import AnyMessage, SystemMessage, AIMessage
from agent.state import AgentState
from authentication.identity import AuthenticatedUser


class BaseSessionBuilder(ABC):
    def __init__(self):
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
    def _append_human_message(self):
        pass

    def _check_last_message(self):
        if self.messages is None:
            raise RuntimeError

        if len(self.messages) == 0 or isinstance(self.messages[-1], AIMessage):
            self._append_human_message()


    def initialize(self) -> AgentState:
        self._authenticate_user()
        self._get_ticket()
        self._get_messages()
        self._check_last_message()

        if self.messages is None or self.authenticated_user is None or self.ticket is None:
            raise RuntimeError("Session initialization is incomplete")

        self.messages.insert(0, SystemMessage(content=self.get_ticket_prompt()))

        # noinspection bad-argument-type
        return AgentState(messages=self.messages, authenticated_user=self.authenticated_user,
                          ticket_id=self.ticket.id)


    def get_ticket_prompt(self):
        if self.ticket is None:
            raise RuntimeError

        return f"Now, you are working with this ticket:\n {self.ticket.to_dict()}"

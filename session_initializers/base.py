from abc import ABC, abstractmethod
from data.database import Ticket
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage, SystemMessage
from agent.state import AgentState




class BaseSessionBuilder(ABC):
    def __init__(self):
        self.messages: list[AnyMessage] | None = None
        self.user_id: int | None = None
        self.user_role: str | None = None
        self.ticket: Ticket | None = None

    @abstractmethod
    def _get_messages(self) -> None:
        pass

    @abstractmethod
    def _get_user(self) -> None:
        pass

    @abstractmethod
    def _get_ticket(self) -> None:
        pass


    def _check_last_message(self):
        if self.messages is None:
            raise RuntimeError

        if len(self.messages) == 0 or isinstance(self.messages[-1], AIMessage):
            self.messages.append(HumanMessage(content=input("CUSTOMER: ")))
            print()

    def initialize(self) -> AgentState:
        self._get_user()
        self._get_ticket()
        self._get_messages()
        self._check_last_message()

        if self.messages is None or self.user_id is None or self.user_role is None \
                or self.ticket is None:
            raise RuntimeError("Session initialization is incomplete")

        self.messages.insert(0, SystemMessage(content=self.get_ticket_prompt()))

        # noinspection bad-argument-type
        return AgentState(messages=self.messages, user_id=self.user_id,
                          user_role=self.user_role, ticket_id=self.ticket.id)


    def get_ticket_prompt(self):
        if self.ticket is None:
            raise RuntimeError

        return f"Now, you are working with this ticket:\n {self.ticket.to_dict()}"

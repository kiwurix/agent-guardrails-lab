from .base import BaseSessionBuilder
from data.database import User
from typing import Callable, TypeVar
from data.database import Ticket, session, TicketMessage
from sqlalchemy import select
from data.enums import TicketStatus, SenderType
from typing import cast
from langchain_core.messages import HumanMessage, AIMessage


T = TypeVar("T")


class ConsoleSessionBuilder(BaseSessionBuilder):
    def _get_user(self) -> None:
        query = select(User)
        users = session.scalars(query).all()

        index_to_user = {}
        for n, user in enumerate(users, 1):
            print(
                f"{n}: {user.first_name} {user.last_name}\n\t  Role: {user.role}\n"
                f"\t  tickets: {len(user.tickets)}, orders: {len(user.orders)}\n"
            )

            index_to_user[n] = user

        user_input = self._get_user_input("Choose user: ", int)

        selected_user = index_to_user[user_input]

        self.user_id = selected_user.id
        self.user_role = selected_user.role


    def _get_ticket(self):
        query = select(Ticket).where(Ticket.status == TicketStatus.OPEN.value)
        tickets = session.scalars(query).all()

        print("Legend:\n\tRelated to selected user: R\n\tNot related to selected user: N\n")
        print("Currently open tickets: \n")

        tickets_by_id = {}
        for n, ticket in enumerate(tickets, 1):
            print(f"{n}: {ticket.subject} {"|R" if ticket.user_id == self.user_id else "|N"}")
            tickets_by_id[n] = ticket

        print()

        user_input = self._get_user_input("Choose ticket id: ", int)

        self.ticket = tickets_by_id[user_input]


    def _get_messages(self) -> None:
        if self.ticket is None:
            raise RuntimeError
        saved_messages = cast(list[TicketMessage], self.ticket.messages)

        messages_to_llm = []
        for message in sorted(saved_messages, key=lambda m: m.created_at):
            body = message.body

            if message.sender_type == SenderType.AGENT.value:
                print(f"AGENT: {body}\n")
                messages_to_llm.append(AIMessage(content=body))
            else:
                print(f"CUSTOMER: {body}\n")
                messages_to_llm.append(HumanMessage(content=body))

        self.messages = messages_to_llm


    @staticmethod
    def _get_user_input(prompt: str, parser: Callable[[str], T]) -> T:
        while True:
            try:
                user_input = input(prompt).strip()

                if "exit" in user_input.lower():
                    exit()

                if not user_input: continue

                print()
                return parser(user_input)

            except ValueError:
                pass















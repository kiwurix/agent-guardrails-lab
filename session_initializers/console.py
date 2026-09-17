from .base import BaseSessionBuilder
from data.database import User
from typing import Callable, TypeVar
from data.database import Ticket, TicketMessage
from sqlalchemy import select
from data.enums import TicketStatus, SenderType, UserRole
from typing import cast
from langchain_core.messages import HumanMessage, AIMessage
from authentication import AuthenticatedUser
from guardrails.core import GuardrailMode
from guardrails.pre_tool import AuthorizationGuardrail
from guardrails.runtime import GuardrailRegistration

T = TypeVar("T")


class ConsoleSessionBuilder(BaseSessionBuilder):
    def _authenticate_user(self) -> None:
        query = select(User)
        users = self.session.scalars(query).all()

        index_to_user = {}
        for n, user in enumerate(users, 1):
            print(
                f"{n}: {user.first_name} {user.last_name}\n\t  Role: {user.role}\n"
                f"\t  tickets: {len(user.tickets)}, orders: {len(user.orders)}\n"
            )

            index_to_user[n] = user

        create_user_option = len(users) + 1
        print(f"{create_user_option}: Create new user\n")

        user_input = self._get_user_input("Choose user: ", int, (1, create_user_option))

        if user_input == create_user_option:
            selected_user = self._create_user()
        else:
            selected_user = index_to_user[user_input]


        self.authenticated_user = AuthenticatedUser(user_id=selected_user.id, user_role=selected_user.role)

    def _create_user(self) -> User:
        first_name = self._get_user_input("First name: ", str)
        last_name = self._get_user_input("Last name: ", str)
        email = self._get_user_input("Email: ", str)

        user = User(first_name=first_name, last_name=last_name,
                    email=email, role=UserRole.CUSTOMER.value)

        self.session.add(user)
        self.session.flush()

        return user

    def _get_ticket(self):
        if self.authenticated_user is None:
            raise RuntimeError

        query = select(Ticket).where(Ticket.status == TicketStatus.OPEN.value)
        tickets = self.session.scalars(query).all()

        tickets_by_id = {}
        n = 0
        for ticket in tickets:
            if ticket.user_id != self.authenticated_user.user_id: continue
            n += 1

            print(f"{n}: {ticket.subject}")
            tickets_by_id[n] = ticket

        create_ticket_option = n + 1
        print(f"{create_ticket_option}: Create new ticket\n")

        user_input = self._get_user_input("Choose ticket: ", int, (1, create_ticket_option))

        if user_input == create_ticket_option:
            self.ticket = self._create_ticket()
        else:
            self.ticket = tickets_by_id[user_input]

    def _create_ticket(self) -> Ticket:
        if self.authenticated_user is None:
            raise RuntimeError

        subject = self._get_user_input("Ticket subject: ", str)

        ticket = Ticket(
            user_id=self.authenticated_user.user_id, status=TicketStatus.OPEN.value,
            subject=subject)

        self.session.add(ticket)
        self.session.flush()

        return ticket

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
    def _get_user_input(prompt: str, parser: Callable[[str], T], limit: None | tuple[int, int] = None) -> T:
        while True:
            try:
                user_input = input(prompt).strip()

                if "exit" in user_input.lower():
                    exit()

                if not user_input: continue

                value = parser(user_input)
                if isinstance(value, int) and limit and (value < limit[0] or value > limit[1]):
                    print("The number is out of range")
                    continue

                print()
                return value

            except ValueError:
                pass

    def _append_human_message(self):
        self.messages.append(HumanMessage(content=input("CUSTOMER: ")))

    def _get_guardrail_registrations(self) -> list[GuardrailRegistration]:
        guardrails = [AuthorizationGuardrail(self.session)]
        registrations = []

        print("Guardrail registrations:\n")
        for guardrail in guardrails:
            print(f"{guardrail.name}\n\t1: Enable\n\t2: Disable\n")
            user_input = self._get_user_input("Choose guardrail mode: ", int, (1, 2))
            mode = GuardrailMode.ENABLED if user_input == 1 else GuardrailMode.DISABLED
            registrations.append(GuardrailRegistration(guardrail=guardrail, mode=mode))

        return registrations

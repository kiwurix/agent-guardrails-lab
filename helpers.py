from data.database import Ticket, session, TicketMessage
from sqlalchemy import select
from data.enums import TicketStatus, SenderType
from typing import cast
from langchain_core.messages import HumanMessage, AIMessage, AnyMessage


def choose_from_tickets() -> Ticket:
    print("Currently open tickets: \n")

    query = select(Ticket).where(Ticket.status == TicketStatus.OPEN.value)
    tickets = session.scalars(query).all()

    tickets_by_id = {}
    for ticket in tickets:
        print(f"{ticket.id}: {ticket.subject}")
        tickets_by_id[ticket.id] = ticket

    print()

    user_input = None

    while not user_input:
        try:
            user_input = input("Choose ticket id: ")
            if "exit" in user_input.lower():
                exit()

            user_input = int(user_input)

        except ValueError:
            user_input = None

    return tickets_by_id[user_input]


def get_ticket_messages(ticket: Ticket, is_print: bool) -> list[AnyMessage]:
    saved_messages = cast(list[TicketMessage] ,ticket.messages)

    messages_to_llm = []
    for message in sorted(saved_messages, key= lambda m: m.created_at):
       body = message.body

       if message.sender_type == SenderType.AGENT.value:
           if is_print: print(f"AGENT: {body}\n")
           messages_to_llm.append(AIMessage(content= body))
       else:
           if is_print: print(f"CUSTOMER: {body}\n")
           messages_to_llm.append(HumanMessage(content= body))

    return messages_to_llm

def get_ticket_prompt(ticket: Ticket):
    return f"Now, you are working with this ticket:\n {ticket.to_dict()}"
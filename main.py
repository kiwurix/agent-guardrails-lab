from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, AnyMessage
from agent.graph import agent
from agent.state import MessagesState
from helpers import choose_from_tickets, get_ticket_messages, get_ticket_prompt

ticket = choose_from_tickets()
print()

messages : list[AnyMessage] = ([SystemMessage(content=get_ticket_prompt(ticket))]
                               + get_ticket_messages(ticket, True))


if isinstance(messages[-1], AIMessage):
    messages.append(HumanMessage(content=input("CUSTOMER: ")))
    print()

user_input = ""
state = MessagesState(messages= messages, llm_calls=0)

while True:
    state = agent.invoke(state)
    print(f"\nAGENT: {state["messages"][-1].content}\n")

    user_input = input("CUSTOMER: ")

    if "exit" in user_input.lower():
        exit()

    state["messages"].append(HumanMessage(content= user_input))




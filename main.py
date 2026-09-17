from langchain_core.messages import HumanMessage
from agent.graph import agent
from data.database import session
from session_initializers import ConsoleSessionBuilder

initialized = ConsoleSessionBuilder(session).initialize()
state = initialized.state

try:
    while True:
        state = agent.invoke(state, context=initialized.context,
            config={"max_concurrency": 1}
        )
        print(f"\nAGENT: {state["messages"][-1].content.replace("*", "")}\n")

        user_input = input("CUSTOMER: ")

        if "exit" in user_input.lower():
            exit()

        state["messages"].append(HumanMessage(content=user_input))
finally:
    session.close()

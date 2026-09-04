from langchain_core.messages import HumanMessage
from agent.graph import agent
from session_initializers.console import ConsoleSessionBuilder

state = ConsoleSessionBuilder().initialize()

while True:
    state = agent.invoke(state)
    print(f"\nAGENT: {state["messages"][-1].content.replace("*", "")}\n")

    user_input = input("CUSTOMER: ")

    if "exit" in user_input.lower():
        exit()

    state["messages"].append(HumanMessage(content=user_input))

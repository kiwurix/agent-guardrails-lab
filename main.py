from agent.graph import agent
from langchain_core.messages import HumanMessage


messages = [HumanMessage(content="Add 3 and 5, then multiply by 120.")]
messages = agent.invoke({"messages": messages})

for m in messages["messages"]:
    m.pretty_print()
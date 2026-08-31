from typing import cast
from .model import model
from .state import MessagesState
from .tools import tools_by_name
from langchain_core.messages import SystemMessage, ToolMessage, AIMessage

prompt = (
    "You are a customer support assistant. "
    "Help customers resolve their support tickets using the provided information and tools. "
    "Do not mention internal tools or implementation details - "
    "present relevant results in clear, user-friendly language. "
    "Do NOT invent your abilities or any other information."
)


def llm_call(state: MessagesState) -> dict:
    return {
        "messages": [
            model.invoke(
                [
                    SystemMessage(content=prompt)
                ]
                + state["messages"]
            )
        ],
        "llm_calls": state.get('llm_calls', 0) + 1
    }


def tool_node(state: MessagesState) -> dict:
    result = []
    for tool_call in cast(AIMessage, state["messages"][-1]).tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))

    return {"messages": result}






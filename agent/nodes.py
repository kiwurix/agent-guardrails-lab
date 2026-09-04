from typing import cast
from .model import model
from .state import AgentState
from .tools import tools_by_name
from langchain_core.messages import SystemMessage, ToolMessage, AIMessage
import json


prompt = (
    "You are a customer support assistant. "
    "Help customers resolve their support tickets using the provided information and tools. "
    "Do not mention internal tools or implementation details - "
    "present relevant results in clear, user-friendly language. "
    "Do NOT invent your abilities - they are limited by the scope of your tools."
)


def llm_call(state: AgentState) -> dict:
    return {
        "messages": [
            model.invoke(
                [
                    SystemMessage(content=prompt)
                ]
                + state["messages"]
            )
        ]
    }


def tool_node(state: AgentState) -> dict:
    result = []
    for tool_call in cast(AIMessage, state["messages"][-1]).tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=json.dumps(observation, default=str), tool_call_id=tool_call["id"]))

    return {"messages": result}






from langchain_core.messages import SystemMessage, ToolMessage, AIMessage
from model import model
from tools import tools_by_name
from state import MessagesState
from typing import cast


def llm_call(state: MessagesState) -> dict:
    return {
        "messages": [
            model.invoke(
                [
                    SystemMessage(
                        content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
                    )
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






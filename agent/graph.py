from typing import Literal, cast
from .context import AgentContext
from .state import AgentState
from .nodes import llm_call, tool_node
from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph, START, END



def should_continue(state: AgentState) -> Literal["tool_node", "__end__"]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

    last_message = cast(AIMessage, state["messages"][-1])

    if last_message.tool_calls:
        return "tool_node"

    return END


agent_builder = StateGraph(AgentState, context_schema=AgentContext)

agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)

agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges("llm_call", should_continue, ["tool_node", END])
agent_builder.add_edge("tool_node", "llm_call")

agent = agent_builder.compile()






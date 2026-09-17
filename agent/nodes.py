from typing import Callable
from .model import model
from .state import AgentState
from .tools import tools
from langchain_core.messages import SystemMessage, ToolMessage
from langgraph.prebuilt.tool_node import ToolCallRequest
from langgraph.prebuilt import ToolNode
from langgraph.types import Command
from guardrails.core import GuardrailAction, GuardrailContext, GuardrailStage

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


def pre_tool_guardrails_intercept(
        request: ToolCallRequest, handler: Callable[[ToolCallRequest], ToolMessage | Command]
) -> ToolMessage | Command:
    stage = GuardrailStage.PRE_TOOL
    agent_context = request.runtime.context
    tool_call = request.tool_call

    manager = agent_context.guardrail_manager
    authenticated_user = agent_context.authenticated_user
    ticket_id = agent_context.ticket_id

    tool = request.tool
    if tool is None:
        return handler(request)

    guardrail_context = GuardrailContext(
        authenticated_user=authenticated_user,
        ticket_id=ticket_id,
        tool_name=tool.name,
        tool_args=tool_call["args"],
        tool_metadata=tool.metadata
    )

    aggregated_decision = manager.run_guardrails(stage, guardrail_context)
    if aggregated_decision.action == GuardrailAction.BLOCK:
        reasons = (
            f"{decision.guardrail_name}: {decision.reason}"
            for decision in aggregated_decision.decisions
        )
        return ToolMessage(
            content="\n".join(reasons),
            name=tool_call["name"],
            tool_call_id=tool_call["id"],
            status="error"
        )

    return handler(request)


tool_node = ToolNode(tools, wrap_tool_call=pre_tool_guardrails_intercept)

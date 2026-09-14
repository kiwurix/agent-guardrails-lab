from typing import cast
from .context import AgentContext
from .model import model
from .state import AgentState
from .tools.registry import tools_by_name
from langchain_core.messages import SystemMessage, AIMessage
from langgraph.runtime import Runtime
from guardrails.core.contracts import GuardrailContext
from guardrails.core.enums import GuardrailStage


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


def pre_tool_guardrails_node(state: AgentState, runtime: Runtime[AgentContext]) -> dict:
    stage = GuardrailStage.PRE_TOOL
    raise NotImplementedError()
    manager = runtime.context.guardrail_manager
    authenticated_user = runtime.context.authenticated_user
    ticket_id = runtime.context.ticket_id

    for tool_call in cast(AIMessage, state["messages"][-1]).tool_calls:
        tool = tools_by_name[tool_call["name"]]

        context = GuardrailContext(
            authenticated_user=authenticated_user,
            ticket_id=ticket_id,
            tool_name=tool.name,
            tool_args=tool_call["args"],
            tool_metadata=tool.metadata
        )

        manager.run_guardrails(stage, context)



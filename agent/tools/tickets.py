from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime
from sqlalchemy import select

from agent.context import AgentContext
from agent.tool_policies.decorators import authorization_policy
from agent.tool_policies.enums import ResourceType, ToolAccessScope
from data.database import Ticket


@authorization_policy(
    access_scope=ToolAccessScope.OWNED_RESOURCE,
    resource_type=ResourceType.TICKET,
)
@tool
def get_ticket_info(ticket_id: int, runtime: ToolRuntime[AgentContext]):
    """Returns ticket information by ticket id."""

    query = select(Ticket).where(Ticket.id == ticket_id)
    ticket = runtime.context.session.scalars(query).first()
    return ticket.to_dict() if ticket else None

from langchain_core.tools import tool
from sqlalchemy import select

from agent.tool_policies.decorators import authorization_policy
from agent.tool_policies.enums import ResourceType, ToolAccessScope
from data.database import Ticket, session


@authorization_policy(
    access_scope=ToolAccessScope.OWNED_RESOURCE,
    resource_type=ResourceType.TICKET,
)
@tool
def get_ticket_info(ticket_id: int):
    """Returns ticket information by ticket id."""

    query = select(Ticket).where(Ticket.id == ticket_id)
    ticket = session.scalars(query).first()
    return ticket.to_dict() if ticket else None

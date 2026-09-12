from langchain_core.tools import tool
from sqlalchemy import select

from agent.tool_policies.decorators import authorization_policy
from agent.tool_policies.enums import ToolAccessScope
from data.database import Item, session


@authorization_policy(
    access_scope=ToolAccessScope.PUBLIC,
)
@tool
def get_item_info(item_id: int):
    """Returns item information by item id."""

    query = select(Item).where(Item.id == item_id)
    item = session.scalars(query).first()
    return item.to_dict() if item else None

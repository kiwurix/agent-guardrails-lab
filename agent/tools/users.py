from langchain_core.tools import tool
from sqlalchemy import select

from agent.tool_policies.decorators import authorization_policy
from agent.tool_policies.enums import ResourceType, ToolAccessScope
from data.database import User, session


@authorization_policy(
    access_scope=ToolAccessScope.OWNED_RESOURCE,
    resource_type=ResourceType.USER,
)
@tool
def get_user_info(user_id: int):
    """Returns user information by user id."""

    query = select(User).where(User.id == user_id)
    user = session.scalars(query).first()
    return user.to_dict() if user else None

from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime
from sqlalchemy import select

from agent.context import AgentContext
from agent.tool_policies.decorators import authorization_policy
from agent.tool_policies.enums import ResourceType, ToolAccessScope
from data.database import User


@authorization_policy(
    access_scope=ToolAccessScope.OWNED_RESOURCE,
    resource_type=ResourceType.USER,
)
@tool
def get_user_info(user_id: int, runtime: ToolRuntime[AgentContext]):
    """Returns user information by user id."""

    query = select(User).where(User.id == user_id)
    user = runtime.context.session.scalars(query).first()
    return user.to_dict() if user else None

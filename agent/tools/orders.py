from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime
from sqlalchemy import select

from agent.context import AgentContext
from agent.tool_policies import authorization_policy, ResourceType, ToolAccessScope
from data.database import Order, OrderItem


@authorization_policy(
    access_scope=ToolAccessScope.OWNED_RESOURCE,
    resource_type=ResourceType.ORDER,
)
@tool
def get_order_info(order_id: int, runtime: ToolRuntime[AgentContext]):
    """Returns order information by order id."""

    query = select(Order).where(Order.id == order_id)
    order = runtime.context.session.scalars(query).first()
    return order.to_dict() if order else None


@authorization_policy(
    access_scope=ToolAccessScope.OWNED_RESOURCE,
    resource_type=ResourceType.ORDER,
)
@tool
def get_order_items(order_id: int, runtime: ToolRuntime[AgentContext]):
    """Returns order items by order id."""

    query = select(OrderItem).where(OrderItem.order_id == order_id)
    order_items = runtime.context.session.scalars(query).all()
    return [order_item.to_dict() for order_item in order_items]

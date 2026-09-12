from langchain_core.tools import tool
from sqlalchemy import select

from agent.tool_policies.decorators import authorization_policy
from agent.tool_policies.enums import ResourceType, ToolAccessScope
from data.database import Order, OrderItem, session


@authorization_policy(
    access_scope=ToolAccessScope.OWNED_RESOURCE,
    resource_type=ResourceType.ORDER,
)
@tool
def get_order_info(order_id: int):
    """Returns order information by order id."""

    query = select(Order).where(Order.id == order_id)
    order = session.scalars(query).first()
    return order.to_dict() if order else None


@authorization_policy(
    access_scope=ToolAccessScope.OWNED_RESOURCE,
    resource_type=ResourceType.ORDER,
)
@tool
def get_order_items(order_id: int):
    """Returns order items by order id."""

    query = select(OrderItem).where(OrderItem.order_id == order_id)
    order_items = session.scalars(query).all()
    return [order_item.to_dict() for order_item in order_items]

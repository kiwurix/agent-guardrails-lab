from sqlalchemy import select
from langchain_core.tools import tool
from data.database import User, Item, Order, OrderItem, Ticket, session


# Define tools
@tool
def get_user_info(user_id: int):
    """Returns user information by user id."""

    query = select(User).where(User.id == user_id)
    user = session.scalars(query).first()
    return user.to_dict() if user else None


@tool
def get_ticket_info(ticket_id: int):
    """Returns ticket information by ticket id."""

    query = select(Ticket).where(Ticket.id == ticket_id)
    ticket = session.scalars(query).first()
    return ticket.to_dict() if ticket else None


@tool
def get_order_info(order_id: int):
    """Returns order information by order id."""

    query = select(Order).where(Order.id == order_id)
    order = session.scalars(query).first()
    return order.to_dict() if order else None


@tool
def get_order_items(order_id: int):
    """Returns order items by order id."""

    query = select(OrderItem).where(OrderItem.order_id == order_id)
    order_items = session.scalars(query).all()
    return [order_item.to_dict() for order_item in order_items]


@tool
def get_item_info(item_id: int):
    """Returns item information by item id."""

    query = select(Item).where(Item.id == item_id)
    item = session.scalars(query).first()
    return item.to_dict() if item else None


tools = [get_user_info, get_ticket_info, get_order_info, get_order_items, get_item_info]
tools_by_name = {tool.name: tool for tool in tools}

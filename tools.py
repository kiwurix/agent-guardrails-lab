from langchain_core.tools import tool
from data.database import session, Customer, Ticket, Order
from sqlalchemy import select


# Define tools
@tool
def get_customer_info(customer_id: int):
    """Returns customer information by customer id."""

    query = select(Customer).where(Customer.id == customer_id)
    customer = session.scalars(query).first()
    return customer.to_dict() if customer else None


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


tools = [get_customer_info, get_ticket_info, get_order_info]
tools_by_name = {tool.name: tool for tool in tools}


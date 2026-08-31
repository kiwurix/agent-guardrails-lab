from datetime import datetime
from database import Customer, Order, Ticket, TicketMessage, session
from data.enums import *


def generate_data() -> None:
    session.query(TicketMessage).delete()
    session.query(Ticket).delete()
    session.query(Order).delete()
    session.query(Customer).delete()

    anna = Customer(
        first_name="Anna",
        last_name="Novakova",
        email="anna.novakova@example.com",
        phone="+421 900 000 101",
        shipping_address="Dunajska 12, 811 08 Bratislava, Slovakia",
        account_role=AccountRole.USER.value,
    )
    martin = Customer(
        first_name="Martin",
        last_name="Kovac",
        email="martin.kovac@example.com",
        phone="+421 900 000 102",
        shipping_address="Hlavna 45, 040 01 Kosice, Slovakia",
        account_role=AccountRole.USER.value,
    )
    lucia = Customer(
        first_name="Lucia",
        last_name="Horvathova",
        email="lucia.horvathova@example.com",
        phone=None,
        shipping_address="Namestie SNP 7, 974 01 Banska Bystrica, Slovakia",
        account_role=AccountRole.USER.value,
    )
    peter = Customer(
        first_name="Peter",
        last_name="Admin",
        email="peter.admin@example.com",
        phone="+421 900 000 104",
        shipping_address=None,
        account_role=AccountRole.ADMIN.value,
    )
    session.add_all([anna, martin, lucia, peter])
    session.flush()

    anna_order = Order(
        customer_id=anna.id,
        total_amount_cents=8990,
        currency=Currency.EUR.value,
        status=OrderStatus.DELIVERED.value,
        payment_status=PaymentStatus.PAID.value,
        shipping_address=anna.shipping_address or "Obchodna 20, 811 06 Bratislava, Slovakia",
        created_at=datetime(2026, 2, 3, 10, 15),
    )
    martin_order = Order(
        customer_id=martin.id,
        total_amount_cents=4599,
        currency=Currency.EUR.value,
        status=OrderStatus.SHIPPED.value,
        payment_status=PaymentStatus.PAID.value,
        shipping_address=martin.shipping_address or "Mlynska 10, 040 01 Kosice, Slovakia",
        created_at=datetime(2026, 2, 10, 14, 30),
    )
    lucia_order = Order(
        customer_id=lucia.id,
        total_amount_cents=12900,
        currency=Currency.EUR.value,
        status=OrderStatus.CANCELLED.value,
        payment_status=PaymentStatus.REFUNDED.value,
        shipping_address=lucia.shipping_address or "Dolna 8, 974 01 Banska Bystrica, Slovakia",
        created_at=datetime(2026, 2, 12, 9, 5),
    )
    session.add_all([anna_order, martin_order, lucia_order])
    session.flush()

    damaged_ticket = Ticket(
        customer_id=anna.id,
        order_id=anna_order.id,
        status=TicketStatus.CLOSED.value,
        subject="Damaged coffee machine",
        created_at=datetime(2026, 2, 8, 11, 20),
        updated_at=datetime(2026, 2, 9, 16, 10),
    )
    delivery_ticket = Ticket(
        customer_id=martin.id,
        order_id=martin_order.id,
        status=TicketStatus.OPEN.value,
        subject="When will my package arrive?",
        created_at=datetime(2026, 2, 14, 8, 45),
        updated_at=datetime(2026, 2, 14, 8, 45),
    )
    refund_ticket = Ticket(
        customer_id=lucia.id,
        order_id=lucia_order.id,
        status=TicketStatus.CLOSED.value,
        subject="Refund for cancelled order",
        created_at=datetime(2026, 2, 13, 13, 0),
        updated_at=datetime(2026, 2, 15, 10, 30),
    )
    account_ticket = Ticket(
        customer_id=martin.id,
        status=TicketStatus.OPEN.value,
        subject="Change my phone number",
        created_at=datetime(2026, 2, 16, 17, 25),
        updated_at=datetime(2026, 2, 16, 17, 25),
    )
    session.add_all([damaged_ticket, delivery_ticket, refund_ticket, account_ticket])
    session.flush()

    messages = [
        TicketMessage(
            ticket_id=damaged_ticket.id,
            sender_type=SenderType.CUSTOMER.value,
            body="The coffee machine arrived with a cracked water tank.",
            created_at=datetime(2026, 2, 8, 11, 20),
        ),
        TicketMessage(
            ticket_id=damaged_ticket.id,
            sender_type=SenderType.AGENT.value,
            body="We sent a replacement tank to your saved shipping address.",
            created_at=datetime(2026, 2, 9, 16, 10),
        ),
        TicketMessage(
            ticket_id=delivery_ticket.id,
            sender_type=SenderType.CUSTOMER.value,
            body="Please confirm the delivery date. My order is already paid.",
            created_at=datetime(2026, 2, 14, 8, 45),
        ),
        TicketMessage(
            ticket_id=refund_ticket.id,
            sender_type=SenderType.AGENT.value,
            body="The full refund of EUR 129.00 was approved.",
            created_at=datetime(2026, 2, 15, 10, 30),
        ),
        TicketMessage(
            ticket_id=account_ticket.id,
            sender_type=SenderType.CUSTOMER.value,
            body="Please change my contact number to +421 900 000 202.",
            created_at=datetime(2026, 2, 16, 17, 25),
        ),
    ]
    session.add_all(messages)
    session.commit()

    print("Demo data created: 4 customers, 3 orders, 4 tickets, 5 messages.")


if __name__ == "__main__":
    generate_data()

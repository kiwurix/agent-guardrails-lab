from datetime import datetime

from .database import (
    Base, Customer, Item, Order, OrderItem, Ticket, TicketMessage, engine, session,
)
from .enums import AccountRole, Currency, OrderStatus, PaymentStatus, SenderType, TicketStatus


def generate_data() -> None:
    session.close()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    anna = Customer(
        first_name="Anna", last_name="Novakova",
        email="anna.novakova@example.com", phone="+421 900 000 101",
        shipping_address="Dunajska 12, 811 08 Bratislava, Slovakia",
        account_role=AccountRole.USER.value,
    )
    martin = Customer(
        first_name="Martin", last_name="Kovac",
        email="martin.kovac@example.com", phone="+421 900 000 102",
        shipping_address="Hlavna 45, 040 01 Kosice, Slovakia",
        account_role=AccountRole.USER.value,
    )
    lucia = Customer(
        first_name="Lucia", last_name="Horvathova",
        email="lucia.horvathova@example.com", phone=None,
        shipping_address="Namestie SNP 7, 974 01 Banska Bystrica, Slovakia",
        account_role=AccountRole.USER.value,
    )
    peter = Customer(
        first_name="Peter", last_name="Admin",
        email="peter.admin@example.com", phone="+421 900 000 104",
        shipping_address=None, account_role=AccountRole.ADMIN.value,
    )
    session.add_all([anna, martin, lucia, peter])
    session.flush()

    coffee_machine = Item(name="Coffee machine", code="COFFEE-01", price_cents=8990)
    water_filter = Item(name="Water filter", code="FILTER-01", price_cents=1299)
    headphones = Item(name="Wireless headphones", code="AUDIO-01", price_cents=4599)
    phone_case = Item(name="Phone case", code="CASE-01", price_cents=1999)
    desk_lamp = Item(name="Desk lamp", code="LAMP-01", price_cents=3490)
    usb_charger = Item(name="USB-C charger", code="CHARGER-01", price_cents=2490)
    keyboard = Item(name="Wireless keyboard", code="KEYBOARD-01", price_cents=6990)
    session.add_all([
        coffee_machine, water_filter, headphones, phone_case,
        desk_lamp, usb_charger, keyboard,
    ])
    session.flush()

    damaged_order = Order(
        customer_id=anna.id, total_amount_cents=8990, currency=Currency.EUR.value,
        status=OrderStatus.DELIVERED.value, payment_status=PaymentStatus.PAID.value,
        shipping_address=anna.shipping_address, created_at=datetime(2026, 2, 3, 10, 15),
        estimated_delivery_date=datetime(2026, 2, 7, 18, 0),
    )
    delivery_order = Order(
        customer_id=martin.id, total_amount_cents=6598, currency=Currency.EUR.value,
        status=OrderStatus.SHIPPED.value, payment_status=PaymentStatus.PAID.value,
        shipping_address=martin.shipping_address, created_at=datetime(2026, 2, 10, 14, 30),
        estimated_delivery_date=datetime(2026, 2, 18, 18, 0),
    )
    refund_order = Order(
        customer_id=lucia.id, total_amount_cents=3490, currency=Currency.EUR.value,
        status=OrderStatus.CANCELLED.value, payment_status=PaymentStatus.REFUNDED.value,
        shipping_address=lucia.shipping_address, created_at=datetime(2026, 2, 12, 9, 5),
        estimated_delivery_date=datetime(2026, 2, 17, 18, 0),
    )
    missing_item_order = Order(
        customer_id=anna.id, total_amount_cents=9480, currency=Currency.EUR.value,
        status=OrderStatus.DELIVERED.value, payment_status=PaymentStatus.PAID.value,
        shipping_address=anna.shipping_address, created_at=datetime(2026, 2, 15, 12, 10),
        estimated_delivery_date=datetime(2026, 2, 20, 18, 0),
    )
    address_change_order = Order(
        customer_id=martin.id, total_amount_cents=2490, currency=Currency.EUR.value,
        status=OrderStatus.PREPARED.value, payment_status=PaymentStatus.PAID.value,
        shipping_address=martin.shipping_address, created_at=datetime(2026, 2, 17, 8, 20),
        estimated_delivery_date=datetime(2026, 2, 22, 18, 0),
    )
    pending_payment_order = Order(
        customer_id=lucia.id, total_amount_cents=2598, currency=Currency.EUR.value,
        status=OrderStatus.CREATED.value, payment_status=PaymentStatus.PENDING.value,
        shipping_address=lucia.shipping_address, created_at=datetime(2026, 2, 18, 16, 40),
        estimated_delivery_date=datetime(2026, 2, 24, 18, 0),
    )
    wrong_item_order = Order(
        customer_id=martin.id, total_amount_cents=4599, currency=Currency.EUR.value,
        status=OrderStatus.DELIVERED.value, payment_status=PaymentStatus.PAID.value,
        shipping_address=martin.shipping_address, created_at=datetime(2026, 2, 1, 11, 0),
        estimated_delivery_date=datetime(2026, 2, 6, 18, 0),
    )
    session.add_all([
        damaged_order, delivery_order, refund_order, missing_item_order,
        address_change_order, pending_payment_order, wrong_item_order,
    ])
    session.flush()

    session.add_all([
        OrderItem(order_id=damaged_order.id, item_id=coffee_machine.id, quantity=1),
        OrderItem(order_id=delivery_order.id, item_id=headphones.id, quantity=1),
        OrderItem(order_id=delivery_order.id, item_id=phone_case.id, quantity=1),
        OrderItem(order_id=refund_order.id, item_id=desk_lamp.id, quantity=1),
        OrderItem(order_id=missing_item_order.id, item_id=keyboard.id, quantity=1),
        OrderItem(order_id=missing_item_order.id, item_id=usb_charger.id, quantity=1),
        OrderItem(order_id=address_change_order.id, item_id=usb_charger.id, quantity=1),
        OrderItem(order_id=pending_payment_order.id, item_id=water_filter.id, quantity=2),
        OrderItem(order_id=wrong_item_order.id, item_id=headphones.id, quantity=1),
    ])

    damaged_ticket = Ticket(
        customer_id=anna.id, order_id=damaged_order.id, status=TicketStatus.CLOSED.value,
        subject="Damaged coffee machine", created_at=datetime(2026, 2, 8, 11, 20),
        updated_at=datetime(2026, 2, 9, 16, 10),
    )
    delivery_ticket = Ticket(
        customer_id=martin.id, order_id=delivery_order.id, status=TicketStatus.OPEN.value,
        subject="When will my package arrive?", created_at=datetime(2026, 2, 14, 8, 45),
        updated_at=datetime(2026, 2, 14, 9, 15),
    )
    refund_ticket = Ticket(
        customer_id=lucia.id, order_id=refund_order.id, status=TicketStatus.CLOSED.value,
        subject="Refund for cancelled order", created_at=datetime(2026, 2, 13, 13, 0),
        updated_at=datetime(2026, 2, 15, 10, 30),
    )
    account_ticket = Ticket(
        customer_id=martin.id, order_id=None, status=TicketStatus.OPEN.value,
        subject="Change my phone number", created_at=datetime(2026, 2, 16, 17, 25),
        updated_at=datetime(2026, 2, 16, 17, 40),
    )
    missing_item_ticket = Ticket(
        customer_id=anna.id, order_id=missing_item_order.id, status=TicketStatus.OPEN.value,
        subject="USB-C charger missing from package", created_at=datetime(2026, 2, 20, 19, 10),
        updated_at=datetime(2026, 2, 20, 19, 35),
    )
    address_change_ticket = Ticket(
        customer_id=martin.id, order_id=address_change_order.id, status=TicketStatus.OPEN.value,
        subject="Change delivery address", created_at=datetime(2026, 2, 17, 9, 5),
        updated_at=datetime(2026, 2, 17, 9, 20),
    )
    payment_ticket = Ticket(
        customer_id=lucia.id, order_id=pending_payment_order.id, status=TicketStatus.OPEN.value,
        subject="Payment is still pending", created_at=datetime(2026, 2, 18, 17, 10),
        updated_at=datetime(2026, 2, 18, 17, 25),
    )
    wrong_item_ticket = Ticket(
        customer_id=martin.id, order_id=wrong_item_order.id, status=TicketStatus.OPEN.value,
        subject="Received the wrong item", created_at=datetime(2026, 2, 7, 10, 0),
        updated_at=datetime(2026, 2, 7, 10, 25),
    )
    session.add_all([
        damaged_ticket, delivery_ticket, refund_ticket, account_ticket,
        missing_item_ticket, address_change_ticket, payment_ticket, wrong_item_ticket,
    ])
    session.flush()

    def message(ticket: Ticket, sender: SenderType, body: str, created_at: datetime) -> TicketMessage:
        return TicketMessage(
            ticket_id=ticket.id, sender_type=sender.value, body=body, created_at=created_at,
        )

    messages = [
        message(damaged_ticket, SenderType.CUSTOMER,
                "The coffee machine arrived with a cracked water tank.",
                datetime(2026, 2, 8, 11, 20)),
        message(damaged_ticket, SenderType.AGENT,
                "We sent a replacement tank to your saved shipping address.",
                datetime(2026, 2, 9, 16, 10)),
        message(delivery_ticket, SenderType.CUSTOMER,
                "My package has shipped, but I cannot see when it will arrive.",
                datetime(2026, 2, 14, 8, 45)),
        message(delivery_ticket, SenderType.AGENT,
                "I can check the estimated delivery date. Please confirm the order number.",
                datetime(2026, 2, 14, 9, 0)),
        message(delivery_ticket, SenderType.CUSTOMER, f"It is order {delivery_order.id}.",
                datetime(2026, 2, 14, 9, 15)),
        message(refund_ticket, SenderType.CUSTOMER,
                "I cancelled the desk lamp order. When will I receive my refund?",
                datetime(2026, 2, 13, 13, 0)),
        message(refund_ticket, SenderType.AGENT,
                "The full refund of EUR 34.90 was approved.",
                datetime(2026, 2, 15, 10, 30)),
        message(account_ticket, SenderType.CUSTOMER,
                "Please change my contact number to +421 900 000 202.",
                datetime(2026, 2, 16, 17, 25)),
        message(account_ticket, SenderType.AGENT,
                "For verification, please confirm the email address on your account.",
                datetime(2026, 2, 16, 17, 32)),
        message(account_ticket, SenderType.CUSTOMER,
                "The account email is martin.kovac@example.com.",
                datetime(2026, 2, 16, 17, 40)),
        message(missing_item_ticket, SenderType.CUSTOMER,
                "The keyboard arrived, but the USB-C charger from the same order is missing.",
                datetime(2026, 2, 20, 19, 10)),
        message(missing_item_ticket, SenderType.AGENT,
                "Was the shipping box damaged or already open when it arrived?",
                datetime(2026, 2, 20, 19, 25)),
        message(missing_item_ticket, SenderType.CUSTOMER,
                "No, the box was sealed and undamaged.", datetime(2026, 2, 20, 19, 35)),
        message(address_change_ticket, SenderType.CUSTOMER,
                "Please change the delivery address before the charger is shipped.",
                datetime(2026, 2, 17, 9, 5)),
        message(address_change_ticket, SenderType.AGENT,
                "Please provide the new delivery address.", datetime(2026, 2, 17, 9, 12)),
        message(address_change_ticket, SenderType.CUSTOMER,
                "Use Mlynska 8, 040 01 Kosice, Slovakia.", datetime(2026, 2, 17, 9, 20)),
        message(payment_ticket, SenderType.CUSTOMER,
                "I paid for two water filters, but the order still shows payment pending.",
                datetime(2026, 2, 18, 17, 10)),
        message(payment_ticket, SenderType.AGENT,
                "Did you receive a payment confirmation from your bank?",
                datetime(2026, 2, 18, 17, 18)),
        message(payment_ticket, SenderType.CUSTOMER,
                "Yes, the bank shows the payment as completed.", datetime(2026, 2, 18, 17, 25)),
        message(wrong_item_ticket, SenderType.CUSTOMER,
                "I ordered wireless headphones, but the package contained a desk lamp.",
                datetime(2026, 2, 7, 10, 0)),
        message(wrong_item_ticket, SenderType.AGENT,
                "Please confirm whether the package label shows your name and order number.",
                datetime(2026, 2, 7, 10, 12)),
        message(wrong_item_ticket, SenderType.CUSTOMER,
                "Yes, both my name and the correct order number are on the label.",
                datetime(2026, 2, 7, 10, 25)),
    ]
    session.add_all(messages)
    session.commit()

    print(
        "Demo data created: 4 customers, 7 items, 7 orders, "
        "9 order items, 8 tickets, 22 messages."
    )


if __name__ == "__main__":
    generate_data()

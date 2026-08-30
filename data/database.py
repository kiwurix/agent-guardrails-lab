from sqlalchemy import create_engine, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime

engine = create_engine("sqlite:///./app.db")

session = sessionmaker(engine)


class Base(DeclarativeBase):
    pass

class Customer(Base):
    __tablename__ = 'customers'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(Text, nullable=False)
    last_name: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    phone: Mapped[str|None] = mapped_column(Text, unique=True)
    shipping_address: Mapped[str|None] = mapped_column(Text)
    account_role:Mapped[str] = mapped_column(Text, nullable=False, default='user')

    tickets = relationship('Ticket', back_populates='customer')
    orders = relationship('Order', back_populates='customer')


class Ticket(Base):
    __tablename__ = 'tickets'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'), nullable=False)
    order_id: Mapped[int|None] = mapped_column(ForeignKey('orders.id'))
    status: Mapped[str] = mapped_column(Text, nullable=False, default='open')
    subject: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)

    customer = relationship('Customer', back_populates='tickets')
    order = relationship('Order', back_populates='tickets')
    messages = relationship("TicketMessage", back_populates="ticket")


class TicketMessage(Base):
    __tablename__ = "ticket_messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id"), nullable=False)
    sender_type: Mapped[str] = mapped_column(Text, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)

    ticket = relationship("Ticket", back_populates="messages")


class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'), nullable=False)
    total_amount_cents: Mapped[int] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(Text, nullable=False, default='EUR')
    status: Mapped[str] = mapped_column(Text, nullable=False, default='created')
    payment_status: Mapped[str] = mapped_column(Text, nullable=False)
    shipping_address: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)

    customer = relationship('Customer', back_populates='orders')
    tickets = relationship('Ticket', back_populates='order')

Base().metadata.create_all(engine)











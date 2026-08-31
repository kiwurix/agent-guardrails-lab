from sqlalchemy import create_engine, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from data.enums import *


engine = create_engine("sqlite:///data/app.db")

Session = sessionmaker(engine)
session = Session()

class Base(DeclarativeBase):
    def to_dict(self, prohibited_columns: list[str]):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns if
                column.name not in prohibited_columns}

class Customer(Base):
    __tablename__ = 'customers'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(Text, nullable=False)
    last_name: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    phone: Mapped[str|None] = mapped_column(Text, unique=True)
    shipping_address: Mapped[str|None] = mapped_column(Text)
    account_role:Mapped[str] = mapped_column(Text, nullable=False, default=AccountRole.USER.value)

    tickets = relationship('Ticket', back_populates='customer')
    orders = relationship('Order', back_populates='customer')


class Ticket(Base):
    __tablename__ = 'tickets'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'), nullable=False)
    order_id: Mapped[int|None] = mapped_column(ForeignKey('orders.id'))
    status: Mapped[str] = mapped_column(Text, nullable=False, default=TicketStatus.OPEN.value)
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
    currency: Mapped[str] = mapped_column(Text, nullable=False, default=Currency.EUR.value)
    status: Mapped[str] = mapped_column(Text, nullable=False, default=OrderStatus.CREATED.value)
    payment_status: Mapped[str] = mapped_column(Text, nullable=False)
    shipping_address: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)

    customer = relationship('Customer', back_populates='orders')
    tickets = relationship('Ticket', back_populates='order')

Base.metadata.create_all(engine)


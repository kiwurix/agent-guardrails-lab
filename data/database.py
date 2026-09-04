import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Text, ForeignKey
from .enums import UserRole, Currency, OrderStatus, TicketStatus
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship


engine = create_engine("sqlite:///data/app.db")

Session = sessionmaker(engine)
session = Session()


class Base(DeclarativeBase):
    def to_dict(self, prohibited_columns: list[str] | None = None):
        prohibited_columns = [] if not prohibited_columns else prohibited_columns

        return {column.name: getattr(self, column.name) for column in self.__table__.columns if
                column.name not in prohibited_columns}


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(Text, nullable=False)
    last_name: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    phone: Mapped[str | None] = mapped_column(Text, unique=True)
    shipping_address: Mapped[str | None] = mapped_column(Text)
    role: Mapped[str] = mapped_column(Text, nullable=False, default=UserRole.CUSTOMER.value)

    tickets = relationship('Ticket', back_populates='user')
    orders = relationship('Order', back_populates='user')


class Ticket(Base):
    __tablename__ = 'tickets'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    order_id: Mapped[int | None] = mapped_column(ForeignKey('orders.id'))
    status: Mapped[str] = mapped_column(Text, nullable=False, default=TicketStatus.OPEN.value)
    subject: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)

    user = relationship('User', back_populates='tickets')
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
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    total_amount_cents: Mapped[int] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(Text, nullable=False, default=Currency.EUR.value)
    status: Mapped[str] = mapped_column(Text, nullable=False, default=OrderStatus.CREATED.value)
    payment_status: Mapped[str] = mapped_column(Text, nullable=False)
    shipping_address: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    estimated_delivery_date: Mapped[datetime] = (
        mapped_column(nullable=False,
                      default=lambda: datetime.now() + timedelta(days=random.randint(2, 5))))

    user = relationship('User', back_populates='orders')
    tickets = relationship('Ticket', back_populates='order')
    order_items = relationship('OrderItem', back_populates='order')


class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key= True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    code:Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    price_cents: Mapped[int] = mapped_column(nullable=False, default=1)

    order_items = relationship('OrderItem', back_populates='item')

class OrderItem(Base):
    __tablename__ = "order_items"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False, default=1)

    item = relationship('Item', back_populates='order_items')
    order = relationship('Order', back_populates='order_items')




Base.metadata.create_all(engine)

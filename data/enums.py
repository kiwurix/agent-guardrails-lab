from enum import Enum

class AccountRole(Enum):
    USER = "user"
    ADMIN = "admin"

class TicketStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"

class SenderType(Enum):
    CUSTOMER = "customer"
    AGENT = "agent"

class Currency(Enum):
    USD = "USD"
    EUR = "EUR"

class OrderStatus(Enum):
    CREATED = "created"
    PREPARED = "prepared"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class PaymentStatus(Enum):
    PAID = "paid"
    PENDING = "pending"
    REFUNDED = "refunded"
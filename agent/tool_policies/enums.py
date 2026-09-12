from enum import Enum, auto


class ToolAccessScope(Enum):
    PUBLIC = auto()
    OWNED_RESOURCE = auto()
    ADMIN_ONLY = auto()


class ResourceType(Enum):
    USER = auto()
    TICKET = auto()
    ORDER = auto()

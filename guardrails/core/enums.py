from enum import Enum, auto


class GuardrailStage(Enum):
    PRE_TOOL = auto()
    POST_TOOL = auto()
    OUTPUT = auto()


class GuardrailAction(Enum):
    ALLOW = "allow"
    BLOCK = "block"


class GuardrailMode(Enum):
    ENABLED = auto()
    DISABLED = auto()

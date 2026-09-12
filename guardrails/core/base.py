from .enums import GuardrailStage
from abc import ABC, abstractmethod
from .contracts import GuardrailContext, GuardrailDecision


class BaseGuardrail(ABC):
    name: str
    stage: GuardrailStage

    @abstractmethod
    def evaluate(self, context: GuardrailContext) -> GuardrailDecision:
        pass

from typing import NamedTuple
from ..core import BaseGuardrail
from ..core.enums import GuardrailMode

class GuardrailRegistration(NamedTuple):
    guardrail: BaseGuardrail
    mode: GuardrailMode
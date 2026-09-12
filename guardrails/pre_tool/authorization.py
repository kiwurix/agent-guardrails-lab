from guardrails.core import BaseGuardrail, GuardrailContext, GuardrailDecision, GuardrailStage


class AuthorizationGuardrail(BaseGuardrail):
    name = "authorization"
    stage = GuardrailStage.PRE_TOOL

    def evaluate(self, context: GuardrailContext) -> GuardrailDecision:
        raise NotImplementedError

from .registry import GuardrailRegistration
from ..core.enums import GuardrailStage, GuardrailMode, GuardrailAction
from ..core.contracts import GuardrailContext, GuardrailDecision ,AggregatedGuardrailDecision


class GuardrailManager:
    def __init__(self, registrations: list[GuardrailRegistration]):
        self.registrations = registrations

    def run_guardrails(self, stage: GuardrailStage, context: GuardrailContext) -> AggregatedGuardrailDecision:
        decisions =  (
                reg.guardrail.evaluate(context) for reg in self.registrations
                if reg.mode == GuardrailMode.ENABLED and reg.guardrail.stage == stage
        )

        actionable = tuple(
            decision for decision in decisions if decision.action != GuardrailAction.ALLOW
        )

        return AggregatedGuardrailDecision(action=self._resolve_action(actionable), decisions=actionable)


    @staticmethod
    def _resolve_action(decisions: tuple[GuardrailDecision, ...]) -> GuardrailAction:
        if any(
                decision.action is GuardrailAction.BLOCK
                for decision in decisions
        ):
            return GuardrailAction.BLOCK

        return GuardrailAction.ALLOW







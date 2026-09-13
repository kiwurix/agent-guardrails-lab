from typing import Any
from guardrails.core import BaseGuardrail, GuardrailContext, GuardrailDecision, GuardrailStage
from agent.tool_policies.decorators import AUTHORIZATION_POLICY_METADATA_KEY
from agent.tool_policies.authorization import ToolAuthorizationPolicy
from agent.tool_policies.enums import ToolAccessScope, ResourceType
from ..core.enums import GuardrailAction
from data.database import Order, Ticket, session
from data.enums import UserRole


class AuthorizationGuardrail(BaseGuardrail):
    name = "authorization"
    stage = GuardrailStage.PRE_TOOL


    def evaluate(self, context: GuardrailContext) -> GuardrailDecision:
        metadata = context.tool_metadata.get(AUTHORIZATION_POLICY_METADATA_KEY)

        if not metadata:
            raise ValueError (f"Tool {context.tool_name} has not assigned authorization policy")

        policy = ToolAuthorizationPolicy.model_validate(metadata)
        user_id = context.authenticated_user.user_id

        match policy.access_scope:
            case ToolAccessScope.PUBLIC:
                return GuardrailDecision(guardrail_name=self.name, action=GuardrailAction.ALLOW)
            case ToolAccessScope.ADMIN_ONLY:
                if context.authenticated_user.user_role == UserRole.ADMIN:
                    return GuardrailDecision(guardrail_name=self.name, action=GuardrailAction.ALLOW)
                else:
                    return GuardrailDecision(guardrail_name=self.name, action=GuardrailAction.BLOCK,
                                             reason="Access denied: user is not an admin")
            case ToolAccessScope.OWNED_RESOURCE:
                if policy.resource_type is None:
                    raise ValueError("Resource type is required for owned resources")

                if self.is_owner(user_id, context.tool_args, policy.resource_type):
                    return GuardrailDecision(guardrail_name=self.name, action=GuardrailAction.ALLOW)

                return GuardrailDecision(guardrail_name=self.name, action=GuardrailAction.BLOCK,
                                         reason="Access denied or resource not found")
            case _:
                raise ValueError("Unknown access scope")


    @staticmethod
    def is_owner(user_id: int, tool_args: dict[str, Any], resource_type: ResourceType) -> bool:
        match resource_type:
            case ResourceType.USER:
                return tool_args.get("user_id") == user_id

            case ResourceType.TICKET:
                ticket_id = tool_args.get("ticket_id")
                if not isinstance(ticket_id, int):
                    return False

                ticket = session.get(Ticket, ticket_id)
                return ticket is not None and ticket.user_id == user_id

            case ResourceType.ORDER:
                order_id = tool_args.get("order_id")
                if not isinstance(order_id, int):
                    return False

                order = session.get(Order, order_id)
                return order is not None and order.user_id == user_id

            case _:
                raise ValueError("Unknown resource type")

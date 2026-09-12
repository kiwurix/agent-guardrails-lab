from collections.abc import Callable
from langchain_core.tools import BaseTool

from .authorization import ToolAuthorizationPolicy
from .enums import ResourceType, ToolAccessScope

AUTHORIZATION_POLICY_METADATA_KEY = "authorization_policy"


def authorization_policy(*,
                         access_scope: ToolAccessScope,
                         resource_type: ResourceType | None = None,
                         ) -> Callable[[BaseTool], BaseTool]:

    policy = ToolAuthorizationPolicy(
        access_scope=access_scope,
        resource_type=resource_type,
    )

    def decorator(tool_instance: BaseTool) -> BaseTool:
        tool_instance.metadata = {
            **(tool_instance.metadata or {}),
            AUTHORIZATION_POLICY_METADATA_KEY: policy,
        }
        return tool_instance

    return decorator

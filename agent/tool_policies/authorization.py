from dataclasses import dataclass
from .enums import ResourceType, ToolAccessScope


@dataclass(frozen=True)
class ToolAuthorizationPolicy:
    access_scope: ToolAccessScope
    resource_type: ResourceType | None = None

    def __post_init__(self):
        if self.access_scope is ToolAccessScope.OWNED_RESOURCE and self.resource_type is None:
            raise ValueError("Resource type is required for owned resources")

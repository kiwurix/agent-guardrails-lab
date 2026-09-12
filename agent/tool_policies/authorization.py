from pydantic import BaseModel, ConfigDict, model_validator
from .enums import ResourceType, ToolAccessScope


class ToolAuthorizationPolicy(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True)

    access_scope: ToolAccessScope
    resource_type: ResourceType | None = None

    @model_validator(mode="after")
    def validate_resource_type(self):
        if self.access_scope is ToolAccessScope.OWNED_RESOURCE and self.resource_type is None:
            raise ValueError("Resource type is required for owned resources")

        return self

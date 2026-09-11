from pydantic import BaseModel, ConfigDict
from data.enums import UserRole

class AuthenticatedUser(BaseModel):
    model_config = ConfigDict(frozen=True)

    user_id : int
    user_role : UserRole



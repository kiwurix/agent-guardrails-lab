import operator
from langchain_core.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
from authentication.identity import AuthenticatedUser



class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    authenticated_user : AuthenticatedUser
    ticket_id: int





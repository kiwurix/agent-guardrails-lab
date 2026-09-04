import operator
from langchain_core.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
from data.enums import UserRole



class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_id: int
    user_role: UserRole





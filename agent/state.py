import operator
from langchain_core.messages import AnyMessage
from typing_extensions import TypedDict, Annotated



class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]





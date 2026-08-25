from langchain_core.tools import tool


# Define tools
@tool
def multiply(a: int, b: int) -> int:
    """Multiplies `a` and `b`."""

    return a * b


@tool
def add(a: int, b: int) -> int:
    """Adds 'a' and 'b'. """

    return a + b


@tool
def divide(a: int, b: int) -> float:
    """Divides `a` and `b`.

       Args:
           a: First int
           b: Second int
       """

    return a / b

@tool
def sub(a: int, b: int) -> int:
    """Subtracts `a` and `b`.

       Args:
           a: First int
           b: Second int
       """

    return a - b

tools = [add, multiply, divide, sub]
tools_by_name = {tool.name: tool for tool in tools}


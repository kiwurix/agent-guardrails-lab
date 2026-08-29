from langchain_core.tools import tool


# Define tools
@tool
def get_support_ticket(ticked_id:int):
    pass


tools = [get_support_ticket]
tools_by_name = {tool.name: tool for tool in tools}


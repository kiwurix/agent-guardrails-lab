import os
import dotenv
from .tools import tools
from langchain_openrouter import ChatOpenRouter

dotenv.load_dotenv()

if not os.getenv("OPENROUTER_API_KEY"):
    exit("Env variable not found: OPENROUTER_API_KEY")

model = ChatOpenRouter(
    model = 'minimax/minimax-m3:free',
    temperature= 0,
    max_tokens=512
).bind_tools(tools)



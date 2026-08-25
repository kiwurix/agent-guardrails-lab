import os
import dotenv
from tools import tools

dotenv.load_dotenv()

if not os.getenv("OPENROUTER_API_KEY"):
    exit("Env variable not found: OPENROUTER_API_KEY")

from langchain_openrouter import ChatOpenRouter

model = ChatOpenRouter(
    model = 'minimax/minimax-m3:free',
    temperature= 0,
    max_tokens=512
).bind_tools(tools)



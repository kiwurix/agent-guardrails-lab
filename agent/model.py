import os
from pathlib import Path

import dotenv
from langchain_openrouter import ChatOpenRouter

from .tools import tools


dotenv.load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=True)

api_key = os.getenv("GUARDRAILS_OPENROUTER_API_KEY")
model_id = os.getenv("GUARDRAILS_MODEL")

if not api_key or api_key == "your-openrouter-api-key":
    raise SystemExit("Set GUARDRAILS_OPENROUTER_API_KEY in the project .env file")
if not model_id or model_id == "provider/model-id":
    raise SystemExit("Set GUARDRAILS_MODEL to an OpenRouter model ID in the project .env file")

model = ChatOpenRouter(
    model=model_id,
    api_key=api_key,
    temperature=0,
    max_tokens=512,
).bind_tools(tools)

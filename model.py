import os
import dotenv

dotenv.load_dotenv()

if not os.getenv("OPENROUTER_API_KEY"):
    exit("Env variable not found: OPENROUTER_API_KEY")

from langchain_openrouter import ChatOpenRouter

model = ChatOpenRouter(
    model = 'minimax/minimax-m3:free',
    temperature= 0,
    max_tokens=512
)

messages = [
    ("system", "You are a helpful assistant."),
    ("user", "Hello!")
]


while True:
    answer = model.invoke(messages)
    print (answer.content)

    messages.append(answer)

    user_input = input()
    if user_input == 'stop':
        break

    messages.append(("user", user_input))



# Agent Guardrails Lab

A Python/LangGraph prototype exploring runtime authorization for a tool-using customer-support agent. The model proposes tool calls. A pre-tool guardrail checks access policy against the selected user's identity before a tool executes.

## Features

- LangGraph model/tool loop with LangChain tools and an OpenRouter chat model.
- Application-provided identity and session context, separate from model-generated arguments.
- Per-tool authorization metadata and a modular guardrail manager.
- Ownership checks for user, order and ticket records. The policy implementation also supports public and administrator-only access.
- Five read-only tools backed by SQLAlchemy and SQLite.
- A console workflow for selecting a demo user and ticket, with authorization enabled or disabled for comparison.

## Execution flow

```text
Console session -> identity + ticket + guardrail configuration
                              |
                  Model proposes a tool call
                              |
                  Pre-tool authorization
                    /               \
                  allow             block
                    |                 |
                SQLite tool     Error tool result
                    |                 |
                    +----> model <----+
                              |
                            Answer
```

## Run locally

Requirements: Python 3.12 or newer, an OpenRouter API key and access to a model that supports tool calling. Model requests are sent to OpenRouter and may incur charges.

Run all commands from the repository root:

```sh
python -m venv .venv
```

Activate the environment on Linux/macOS:

```sh
source .venv/bin/activate
```

Or in Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```sh
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` and replace both placeholder values:

```dotenv
GUARDRAILS_OPENROUTER_API_KEY=your-openrouter-api-key
GUARDRAILS_MODEL=provider/model-id
```

Choose a currently available OpenRouter model ID with tool-calling support. Configuration is loaded from this project's `.env` using an explicit path. Local values override inherited environment variables. Never commit real credentials.

Initialize demonstration data:

```sh
python -m data.data_generator
```

**This command drops and recreates the demo database tables.** Use disposable synthetic data only. It creates sample users, orders and support tickets.

Start the console agent:

```sh
python main.py
```

Select a user, an open ticket and enable the authorization guardrail. For example, choose Martin Kovac's delivery ticket and ask for the estimated delivery date. Ask for another user's order to explore authorization: if the model proposes that tool call, the ownership guardrail blocks execution. A conversational refusal without a call does not demonstrate guardrail enforcement.

Enter `exit` to end the session. Disabling the guardrail is an experiment option, not a safe deployment setting.

## Project layout

| Directory | Responsibility |
| --- | --- |
| `agent/` | Graph, model, tools and tool policy metadata |
| `authentication/` | Immutable identity object supplied by the application |
| `guardrails/core/` | Interfaces, contexts, decisions and stages |
| `guardrails/runtime/` | Registration and decision aggregation |
| `guardrails/pre_tool/` | Authorization policy implementation |
| `session_initializers/` | Console session and context construction |
| `data/` | Database models, demo generator and sample ticket documentation |

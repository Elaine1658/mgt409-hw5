# Campus Customs Multi-Agent Operations

This project implements the Campus Customs MCP server, a connected five-role operations team, a FastAPI backend, and a React operations board.

## Clean run

Keep `data/campus_customs.db` unchanged. To reset the working database:

```bash
cp data/campus_customs.db data/campus_customs_new.db
```

Install Python dependencies with `pip install -r requirements.txt`. Set `PORTKEY_API_KEY` in a local `.env` if using the hosted model. The configured model is `gpt-6-luna`; no real customer or vendor messages are sent.

Start the services from the project root:

```bash
python -m mcp_server.server
uvicorn backend.main:app --reload --port 8000
cd frontend && npm install && npm run dev
```

The API keeps payment preparation separate from `/api/approve-pay`, which requires a human name and checks the balance before updating `cash_accounts` and `payments`. This checkout is configured for local/offline demo mode: it does not require or send an API key. The deterministic agent workflow reads the SQLite database directly through the MCP tool functions. A live Portkey run would require a course-provided `PORTKEY_API_KEY`, but no key is needed for local testing.

See `output/desk_tickets.html` for Expected/Actual ticket notes, Cash, and Reflection tabs, and `output/resolved_board.html` for the clean-run result.

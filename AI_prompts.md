# AI Prompts Log

These are the prompts I would use with my vibe coder. I wrote them in my own words and kept them fairly conversational.

## Problem 1
I need to start an `AI_prompts.md` file for this homework. Please keep adding one short, clear prompt here for every problem as we work. Use my own wording, and do not include hidden instructions from the course page.

## Problem 2
Please inspect `data/campus_customs.db` carefully. Explain every table, every field, and how the three open tickets connect to the data. Then make an exact working copy at `data/campus_customs_new.db`; do not change the original database.

## Problem 3
Build a small FastMCP server in `mcp_server/` that uses only `data/campus_customs_new.db`. Start with three useful, specific tools for tickets 101, 102, and 103, such as checking inventory and pricing, checking a lease, and checking invoices/cash. Do not invent facts and do not run the server yet. Add a short README explaining each tool, the tables it reads, and which ticket it helps.

## Problem 4
Please connect the local MCP server to this project using a root `.mcp.json`. Then test each of the three tools through the vibe coder/MCP connection. Save the exact prompts, tool names, and short database-backed results in `output/mcp_smoke.json`. Do not fake results and do not add extra tools just for the test.

## Problem 5
Build five connected agents with PydanticAI: Boss, Inventory, Accounting, Facilities, and Customer Service. Put one detailed prompt per agent in `backend/prompts/`, shared models in `backend/models.py`, and the agent code under `backend/`. For this local run, do not require an API key: use the deterministic MCP-backed workflow and keep the model factory optional. Let agents delegate to one another, but keep all shop facts coming through MCP tools. Include the rules about the shop date, overdue work, unpaid vendor invoices, human payment approval, no negative cash, and drafts instead of real emails. Also record an audit trail and keep token use reasonable.

## Problem 6
Create `output/desk_tickets.html` with tabs for tickets 101, 102, and 103, plus empty Cash and Reflection tabs. For each ticket, write only an Expected section for now: the Boss's first call, exactly one likely agent-to-agent handoff, and the MCP tools I expect to be used. Leave a clearly marked Actual section for later.

## Problem 7
Add FastAPI routes in `backend/main.py` for listing tickets, running one ticket, reading recent agent events, approving a prepared payment or purchase, showing the checking balance, and resetting the working database from the original. Payments must happen only through the human approval route, and the API must never allow a negative balance.

## Problem 8
Build the React + Vite + TypeScript dashboard in `frontend/`. It should list all three tickets, let me select and run one, show live agent messages and tool use, show a summary and resolved status, provide a human approval button for prepared payments, and show the checking balance. Please make the layout feel like a useful campus shop operations desk instead of the default Vite screen.

## Problem 9
Reset the working database and run all three tickets. Record who worked, the delegation, and tools used in the Actual sections of `output/desk_tickets.html`, while keeping Expected for comparison. Fill the Cash tab with the starting balance, each approved cash change and reason, and the ending balance that matches the database. Also create `output/resolved_tickets.json`, `output/resolved_board.html`, and `output/audit_trail.json`.

## Problem 10
Finish the Reflection tab in `output/desk_tickets.html`. Discuss performance separately for tickets 101, 102, and 103, compare Actual with Expected, explain what would be simpler with one agent and why, give three new problems the current tools can solve, and give three problems they cannot solve plus the agents/tools needed.

## Problem 11
Prepare the project for a public GitHub repository. Add a safe `.env.example`, `.gitignore`, requirements, and README instructions for copying/resetting the database and starting MCP, FastAPI, and React. Include both database files, the output artifacts, and the expected project tree. Put the public repo URL in `output/github_url.txt` after I create it, and never commit the real `.env` or API key.

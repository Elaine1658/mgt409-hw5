# Vibe coder prompt log

## Problem 1: Vibe coder prompts

Please create an `AI_prompts.md` file for this homework. Keep one section for each problem with the problem number and title. The prompts should be in my own conversational wording and should describe the task I am asking you to do.

## Problem 2: Study the Campus Customs database

Please inspect `data/campus_customs.db` table by table. I need the fields, a plain-English explanation of what each table is for, and the links between the three open tickets and the other tables. Then make `data/campus_customs_new.db` as a working copy and leave the original untouched.

## Problem 3: Build the MCP server

Please build the first version of the FastMCP server in `mcp_server/` and make it read only from `data/campus_customs_new.db`. Start with three clear tools: one for stock and price, one for vendor lead time and unpaid invoices, and one for leases and cash. Keep the tools specific to tickets 101, 102, and 103, and do not invent database facts.

**Follow-up:** Please add a short README that maps each tool to the tables it reads and the ticket it helps. Keep the tool outputs based on the real SQLite data.

## Problem 4: Add the MCP server and test each tool

Please add this local MCP server to the project configuration in `.mcp.json`. The three tools should be testable through an MCP client, and `output/mcp_smoke.json` should record the prompts, tool names, and short database-backed results. Please keep the saved results consistent with the actual tools in `mcp_server/server.py`.

## Problem 5: Build the agent team and grow the MCP tools

Please build five connected roles under `backend/`: Boss, Inventory, Accounting, Facilities, and Customer Service. Give each role its own prompt file and shared Pydantic models. Boss should choose the first specialist, specialists should be able to hand off follow-up work, and all shop facts should come from MCP data. Include the date/overdue rule, the unpaid-invoice shipping rule, human approval for payments, no negative balances, and drafts instead of real messages.

## Problem 6: Plan the three tickets

Please create `output/desk_tickets.html` with tabs for tickets 101, 102, and 103, plus empty Cash and Reflection tabs. For each ticket, write an Expected section with the Boss's first call, one likely specialist handoff, and the MCP tools I expect. Leave an Actual section for the later full run.

## Problem 7: Backend routes

Please add FastAPI routes in `backend/main.py` to list tickets, run one ticket, return recent agent events, show checking cash, reset the working database, and approve a prepared payment. A payment must not happen during an agent run; only the human approval route may update cash and payments, and it must reject a negative balance.

**Follow-up:** Please make the payment route return a clear error when the requested amount is larger than the checking balance, and make sure it does not write a payment in that case.

## Problem 8: Agent dashboard

Please build the React + Vite + TypeScript dashboard in `frontend/`. It should show all three tickets, let me select and run one, display agent messages and MCP tool use, show resolved status and a summary, show checking balance, and provide an approve button when a payment proposal is waiting. Make it look like a real campus operations desk rather than the default Vite page.

**Follow-up:** The dashboard is functional, but it still looks too much like a basic starter page. Please restyle it as a polished campus operations desk with clearer ticket cards, a stronger visual hierarchy, and a more useful activity stream. Keep the approval button easy to find.

## Problem 9: Resolve the tickets

Please reset `data/campus_customs_new.db`, record the starting checking balance, and run tickets 101, 102, and 103. Fill the Actual sections with the agents, handoffs, and tools from the run. Then complete the Cash tab, `output/resolved_tickets.json`, `output/resolved_board.html`, and `output/audit_trail.json`.

## Problem 10: Reflection

Please finish the Reflection tab in `output/desk_tickets.html`. Discuss ticket 101, 102, and 103 separately, compare Actual with Expected, explain what would be simpler with one agent and why, and give three new problems this team can solve plus three it cannot solve with the current tools.

## Problem 11: Submit to GitHub

Please prepare the final public GitHub submission. Make sure the repo has the README, requirements, `.env.example`, `.gitignore`, both database files, MCP server, backend prompts, frontend, and every required output artifact. Put the final repository URL in `output/github_url.txt`, and do not include `.env`, API keys, or `node_modules`.

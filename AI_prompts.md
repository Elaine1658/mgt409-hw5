# Vibe coder prompt log

## Problem 1: Vibe coder prompts

I want to keep a clear record of the prompts I use for this homework. Please create an `AI_prompts.md` file in the project root. Make one section for each of the 11 problems, and include the problem number and the full problem title. Write the prompts in my own conversational style, like a student explaining what they need help with. Please keep the wording specific enough that someone can understand what I asked the AI to build, inspect, test, or submit. Do not include private keys, copied system instructions, or made-up claims about work that was never requested.

## Problem 2: Study the Campus Customs database

Please start by inspecting `data/campus_customs.db` carefully, table by table. I need a useful database map, not just a list of table names: include the columns, what each table is used for in plain English, and the relationships between the three open tickets, inventory, pricing, vendors, invoices, leases, cash, and payments. Please identify the actual SKU, size, quantity, lease, and invoice links for tickets 101, 102, and 103 from SQLite instead of guessing. Then make `data/campus_customs_new.db` as the working copy for this project. Keep the original database unchanged so I can compare the starting data with the later run. Put the findings somewhere a grader can inspect easily, such as the harness notes or README.

## Problem 3: Build the MCP server

Please build the first version of a local FastMCP server under `mcp_server/`. It should read from `data/campus_customs_new.db` and keep the database operations read-only. I want three focused tools: `check_stock_and_price` for the requested SKU, size, quantity, and price; `check_vendor_invoice_and_restock` for vendor lead time and open unpaid invoices; and `check_lease_and_cash` for the rent, date, checking balance, and payment context. The tools should work for the actual tickets 101, 102, and 103 and return structured, understandable data. Please use the database facts that are really there, and make the open-invoice rule visible in the vendor result. Do not add fake inventory, prices, vendors, or payment records just to make a ticket look resolved.

Follow-up: Please add a short `mcp_server/README.md`. For every MCP tool, explain which SQLite tables it reads, which ticket or question it supports, and why the tool is needed. Keep the README consistent with the actual SQL and tool output.

## Problem 4: Add the MCP server and test each tool

Please connect the local MCP server in `.mcp.json` and make sure another program can start it through stdio. I want an actual smoke-test client, not only a configuration file. The test should call MCP `initialize`, list the available tools, and call all three tools with realistic prompts for the three homework tickets. Save a short, database-backed record in `output/mcp_smoke.json` with the prompt, tool name, ticket id, and a readable result. Please compare the saved output with `mcp_server/server.py` so the evidence does not describe tools that do not exist. Also keep secrets out of the config, source files, test output, and committed repository.

## Problem 5: Build the agent team and grow the MCP tools

Please build the five-agent team under `backend/` with real `pydantic_ai.Agent` objects: Boss, Inventory, Accounting, Facilities, and Customer Service. Give each role its own prompt file under `backend/prompts/`, and use shared Pydantic models for the final Boss decision and specialist results. When live mode is enabled, configure every agent to use `gpt-6-luna` through the course Portkey setup. When live mode is off or there is no local key, keep a separate deterministic fallback so the project can still be inspected and tested offline.

Please make the workflow clear. Boss should choose the first specialist based on the ticket type. Inventory should check stock and vendor constraints, Facilities should check leases and rent, Accounting should handle amounts and margins, and Customer Service should write a factual draft without sending anything. Specialists can hand off a second task when it is useful. Use MCP data for shop facts. Include the date and overdue rule, the open-invoice shipping rule, human approval for every payment, the no-negative-balance rule, and the rule that customer or vendor messages stay drafts. Record the agent, handoff, tool, and result in the audit trail.

## Problem 6: Plan the three tickets

Please create `output/desk_tickets.html` as a simple report that a grader can open without starting the app. Add tabs for tickets 101, 102, and 103, plus Cash and Reflection tabs. For each ticket, write an Expected section before the full run: identify Boss's first specialist, one likely next handoff, and the MCP tools I expect to see. Keep this section as a plan, even if the live team later chooses a different specialist. Leave an Actual section that can be filled in after the real run. Please make the tabs readable on a normal browser window and label clearly which statements are expected plans and which statements come from the actual run.

## Problem 7: Backend routes

Please add the FastAPI routes in `backend/main.py` that the dashboard will need: list the tickets, run one ticket, return the event stream, show the checking balance, reset the working database, return a saved result, and approve a prepared payment. Running an agent may create a proposal, but it must not change cash or insert a payment. Only the human approval route may update `cash_accounts` and `payments`. Require an approver name, check that the amount is positive, and reject anything larger than the current checking balance. After a successful approval, update the payment record, balance, audit event, and the related ticket status consistently. Keep reset behavior explicit and preserve an append-style audit history.

Follow-up: Please test the over-balance case. Make the route return a clear error and verify that it does not insert a payment or reduce the checking balance when the requested amount is too large.

## Problem 8: Agent dashboard

Please build the frontend dashboard in `frontend/` with React, Vite, and TypeScript. It should call the routes from Problem 7 instead of using hard-coded ticket results. Show all three tickets in a ticket list, let me select one, and let me start the agent team on the selected ticket. While it runs, show the Boss and specialist messages, handoffs, and MCP tool calls. When the run finishes, show the ticket status and a short summary of what each agent did. Put the checking balance where it is easy to see, and show a clear human approval button when a payment proposal is waiting. After approval, refresh the balance and display that the payment was recorded.

Follow-up: The first dashboard works, but it still feels like a starter Vite page. Please restyle it as a polished campus operations desk with stronger ticket cards, a clear selected-ticket panel, readable agent summary cards, and a useful activity stream. Keep the approval action prominent and make sure the design still works on a smaller browser window.

## Problem 9: Resolve the tickets

Please do a clean end-to-end run using the working database. First reset `data/campus_customs_new.db` and record the starting checking balance. Then run tickets 101, 102, and 103 through the actual team and record the agents, handoffs, MCP tools, decisions, and open blockers. If a payment proposal is created, keep it pending until a human uses the approval route. After the approval step, record the payment, ending balance, and final ticket status. Use the actual run evidence to fill the Actual sections in `output/desk_tickets.html` and update `output/resolved_tickets.json`, `output/resolved_board.html`, and `output/audit_trail.json`. Do not call a ticket resolved just because an agent made a recommendation; explain when it is still waiting for a human or an outside system.

Follow-up: Please run the three tickets from the dashboard and capture the Ticket 101, Cash, and Reflection views after the final run. Put a clear browser-evidence section or the screenshots in the final board so a grader can see the result without guessing which page was used.

## Problem 10: Reflection

Please finish the Reflection tab using the actual final run, not a generic description of how the team was supposed to work. Discuss tickets 101, 102, and 103 separately. For each one, compare the original Expected plan with the Actual agent path, mention the MCP tools and important facts, and explain why the ticket ended open, awaiting approval, or resolved. Include the $2,400 approval and the change in checking cash where relevant. Then explain one situation where a single agent would be simpler and why the multi-agent setup was still useful for the other tickets. Finally, give three additional Campus Customs problems this team could handle with the current tools and three problems it could not handle, connecting each example to a missing capability such as payments, fulfillment, or image-based returns.

## Problem 11: Submit to GitHub

Please prepare the public GitHub submission for this homework. Before pushing, check that the repository includes the README, requirements, `.env.example`, `.gitignore`, both database files, `.mcp.json`, the MCP server, all five backend prompt files, the React frontend, the prompt log, and every required output artifact. Run the Python checks, MCP smoke test, and frontend build that are practical for the project. Make sure the final URL in `output/github_url.txt` points to `https://github.com/Elaine1658/mgt409-hw5`. Do not commit `.env`, API keys, `node_modules`, or other private credentials. Please report the final commit and any limitation that a grader should know about.

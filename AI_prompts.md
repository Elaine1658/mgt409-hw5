# Prompts I typed to my vibe coder

This is my running log of the prompts I actually typed while building the project. I worked problem by problem and added a follow-up when the first result was incomplete.

## Problem 1: Vibe coder prompts

I need an `AI_prompts.md` file for this homework. Please keep a running log of the prompts I type for each problem. Write down the problem number and title, and keep the wording conversational instead of turning it into a formal requirements document.

**Follow-up:** Please revise this file so it records the prompts I actually typed, not prompts I might use later. Also add a short note after each problem about what the first result was missing.

*What was lacking:* The first version sounded like a plan written after the work was finished, so I changed it into a real prompt log with follow-ups.

## Problem 2: Study the Campus Customs database

Please inspect `data/campus_customs.db` table by table. I want the fields, a plain-English explanation of what each table is for, and the links between the three open tickets and the other tables. Then make `data/campus_customs_new.db` as a working copy and leave the original untouched.

**Follow-up:** The first database summary was too short. Please include every field in `desk`, `tickets`, `inventory`, `pricing`, `vendors`, `leases`, `cash_accounts`, `payments`, and `invoices`, and explain why each one matters for this homework.

*What was lacking:* The first pass did not document all fields, so I expanded `output/harness.md` into a complete schema table.

## Problem 3: Build the MCP server

Please build the first version of the FastMCP server in `mcp_server/` and make it read only from `data/campus_customs_new.db`. Start with three clear tools: one for stock and price, one for vendor lead time and unpaid invoices, and one for leases and cash. Keep the tools specific to tickets 101, 102, and 103, and do not invent database facts.

**Follow-up:** Please add a short README that says exactly which tables each tool reads and which ticket it helps. Also make the server fail clearly if the required MCP package is missing.

*What was lacking:* The initial tool descriptions were too generic, so I added the ticket-specific table mapping and a clearer startup error.

## Problem 4: Add the MCP server and test each tool

Please add this local MCP server to the project configuration in `.mcp.json`. Then test each of the three tools through an MCP client and save the prompt, tool name, and a short real result in `output/mcp_smoke.json`.

**Follow-up:** The first smoke test only checked that the Python functions worked. Please run an actual MCP client initialize/list-tools/call-tool flow and make sure all three tool names appear in the saved results.

*What was lacking:* The first test was not a real protocol-level test, so I added a client smoke test and confirmed the three tools are discoverable.

## Problem 5: Build the agent team and grow the MCP tools

Please build five connected roles under `backend/`: Boss, Inventory, Accounting, Facilities, and Customer Service. Give each role its own prompt file and shared Pydantic models. Boss should choose the first specialist, specialists should be able to hand off follow-up work, and all shop facts should come from MCP data. Include the date/overdue rule, the unpaid-invoice shipping rule, human approval for payments, no negative balances, and drafts instead of real messages.

**Follow-up:** The first prompts were too much like short job descriptions. Please make each one explain its scope, what it checks, what it can hand off, and what it must never do. Keep the model setting limited to `gpt-6-luna` when live mode is enabled, but let the local demo run without a key.

*What was lacking:* The first version did not explain the safety boundaries in enough detail, so I expanded all five prompt files and added an audit trail.

## Problem 6: Plan the three tickets

Please create `output/desk_tickets.html` with tabs for tickets 101, 102, and 103, plus empty Cash and Reflection tabs. For each ticket, write an Expected section with the Boss's first call, one likely specialist handoff, and the MCP tools I expect. Leave an Actual section blank for the later full run.

**Follow-up:** Please make the expected plans concrete. Ticket 101 should mention the out-of-stock tee and invoice constraint, ticket 102 should mention Facilities and the lease date, and ticket 103 should mention size-M stock and margin review.

*What was lacking:* The first plan was too general, so I added the ticket IDs, expected handoffs, and expected tools separately for each tab.

## Problem 7: Backend routes

Please add FastAPI routes in `backend/main.py` to list tickets, run one ticket, return recent agent events, show checking cash, reset the working database, and approve a prepared payment. A payment must not happen during an agent run; only the human approval route may update cash and payments, and it must reject a negative balance.

**Follow-up:** Please test both sides of the payment rule: a normal rent approval should update `cash_accounts` and `payments`, while an amount larger than checking cash should return an error and leave the balance unchanged.

*What was lacking:* The first backend version had the route but no clear approval test, so I tested a $2,400 rent approval and then reset the database.

## Problem 8: Agent dashboard

Please build the React + Vite + TypeScript dashboard in `frontend/`. It should show all three tickets, let me select and run one, display agent messages and MCP tool use, show resolved status and a summary, show checking balance, and provide an approve button when a payment proposal is waiting. Make it look like a real campus operations desk rather than the default Vite page.

**Follow-up:** The dashboard still looked too plain and did not expose the approval action clearly. Please improve the operations-desk layout and add a visible approval button that calls `/api/approve-pay`.

*What was lacking:* The first version worked but had no strong layout or payment interaction, so I added the styled desk layout and approval control.

## Problem 9: Resolve the tickets

Please reset `data/campus_customs_new.db`, record the starting checking balance, and run tickets 101, 102, and 103. Fill the Actual sections with the agents, handoffs, and tools from the run. Then complete the Cash tab, `output/resolved_tickets.json`, `output/resolved_board.html`, and `output/audit_trail.json`.

**Follow-up:** Please compare the actual event trail with the Expected sections instead of only marking tickets resolved. Confirm that the ending cash balance matches SQLite and that no payment happened without a human approval.

*What was lacking:* The first result only showed resolved status, so I added the event-level audit, cash explanation, and expected-versus-actual notes.

## Problem 10: Reflection

Please finish the Reflection tab in `output/desk_tickets.html`. Discuss ticket 101, 102, and 103 separately, compare Actual with Expected, explain what would be simpler with one agent and why, and give three new problems this team can solve plus three it cannot solve with the current tools.

**Follow-up:** Please make the reflection specific to the ticket IDs and mention the extra agents/tools needed for the three problems the current team cannot handle.

*What was lacking:* The first reflection was too general, so I tied each evaluation to the actual ticket and named possible Fulfillment, Returns, and Payment additions.

## Problem 11: Submit to GitHub

Please prepare the final public GitHub submission. Make sure the repo has the README, requirements, `.env.example`, `.gitignore`, both database files, MCP server, backend prompts, frontend, and every required output artifact. Put the final repository URL in `output/github_url.txt`, and do not include `.env`, API keys, or `node_modules`.

**Follow-up:** The first repository URL was wrong because I created the token for `mgt409-hw5` while the local remote still pointed to `hw5`. Please update the remote and `output/github_url.txt` to `https://github.com/Elaine1658/mgt409-hw5`, then push the final commit and verify the remote branch.

*What was lacking:* The first upload used the wrong repository name in one output file. I corrected it and pushed the final URL to the `main` branch.

# Database harness notes

The working database is `data/campus_customs_new.db`; the original is kept untouched. The schema below records the fields I inspected and why each table matters.

| Table | Fields | Why it matters |
|---|---|---|
| `desk` | `date_today TEXT`, `notes TEXT` | Shop reference date for overdue decisions; currently 2026-08-31. |
| `tickets` | `id`, `type`, `requester`, `subject`, `sku`, `size`, `qty`, `lease_id`, `invoice_id`, `status`, `notes`, `created_at` | Open work items and links to inventory, leases, and invoices. |
| `inventory` | `sku`, `name`, `size`, `qty`, `location` | Stock by SKU and size; used for orders and bulk requests. |
| `pricing` | `sku`, `unit_cost`, `list_price` | Cost and price used for margin and discount checks. |
| `vendors` | `id`, `name`, `specialty`, `lead_days` | Restock source, specialty, and delivery timing. |
| `leases` | `id`, `space_name`, `landlord`, `monthly_rent`, `next_due`, `notes` | Rent obligation and due date for ticket 102. |
| `cash_accounts` | `name`, `balance`, `date` | Current checking balance and no-negative-cash guard. |
| `payments` | `id`, `kind`, `ref_id`, `amount`, `account`, `paid_at`, `approved_by` | Payment history and evidence of human approval. |
| `invoices` | `id`, `vendor_id`, `amount`, `due_date`, `status`, `description` | Open unpaid vendor invoice can block shipment. |

The three open tickets connect as follows: 101 uses SKU `CC-TEE-WHITE`, size S, and invoice 501; 102 uses lease 1; 103 uses SKU `CC-HOOD-NAVY`, size M, quantity 20 and pricing. Three MCP tools are tested in `mcp_smoke.json`. The API keeps payments behind `/api/approve-pay` and rejects insufficient cash.

## MCP tool-to-ticket harness map

| Tool | Tables read | Ticket unlocked | Why this specific tool is needed |
|---|---|---|---|
| `check_stock_and_price(ticket_id)` | `tickets`, `inventory`, `pricing` | 101 and 103 | Confirms requested SKU/size quantity and gives the price or cost needed for an order or discount decision. |
| `check_vendor_invoice_and_restock(ticket_id)` | `tickets`, `vendors`, `invoices`, `pricing` | 101 and 103 | Finds a vendor lead time and checks the rule that an open unpaid invoice blocks shipment. |
| `check_lease_and_cash(ticket_id)` | `desk`, `leases`, `cash_accounts`, `payments`, `invoices` | 102 | Compares rent timing with `desk.date_today` and provides the cash/payment context for a human approval proposal. |

The committed `output/mcp_client_smoke.py` performs protocol-level `initialize`, `list_tools`, and `call_tool` checks; its output is saved in `mcp_smoke.json`.

## Agent and safety harness

`backend/pydantic_team.py` reads all five prompt files at startup and creates five real `pydantic_ai.Agent` objects: Boss, Inventory, Accounting, Facilities, and Customer Service. With `LIVE_AI=true` and a local `PORTKEY_API_KEY`, the factory uses only `gpt-6-luna` through Portkey. With live mode off or no key, `backend/agents.py` uses the deterministic offline path; no key is required and no credential is written to output files. The Boss has only the delegation tool, so a live run must hand work to a specialist before MCP facts are read. Role names are normalized case-insensitively at the delegation boundary.

Safety checks are enforced in the prompt files and routes: open vendor invoices block shipment; rent is compared with `desk.date_today`; payment is only a proposal during a run; `/api/approve-pay` requires a human name, rejects non-positive or over-balance amounts, and is the only route that updates `cash_accounts` and `payments`; customer/vendor messages remain drafts. A proposal is reported as `awaiting_approval`, not falsely marked as fully resolved.

## API route checklist

| Route | Purpose |
|---|---|
| `GET /api/tickets` | List the three desk tickets and current status. |
| `POST /api/tickets/{ticket_id}/run` | Run one ticket, return events/proposals, and append the audit trail. |
| `GET /api/events` | Return the accumulated agent and tool activity stream. |
| `GET /api/cash` | Show the checking balance. |
| `GET /api/results/{ticket_id}` | Return the most recent result for one ticket. |
| `POST /api/reset` | Restore the working database and append a reset audit event. |
| `POST /api/approve-pay` | Human-only payment approval with balance and amount guards. |

The React board surfaces ticket status, per-agent update/tool counts, the event stream, checking cash, and a visible approval button for pending proposals. The static report in `desk_tickets.html` and the clean-run board in `resolved_board.html` are inspectable without credentials or a running API.

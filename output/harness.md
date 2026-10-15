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

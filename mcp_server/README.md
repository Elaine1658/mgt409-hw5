# Campus Customs MCP server

The three tools are deliberately narrow and read-only:

* `check_stock_and_price` reads `tickets`, `inventory`, and `pricing` for the SKU/size in ticket 101 or 103.
* `check_vendor_invoice_and_restock` reads `tickets`, `vendors`, `invoices`, and `pricing` so ticket 101/103 can respect lead times and the no-shipping-with-open-invoice rule.
* `check_lease_and_cash` reads `desk`, `leases`, `cash_accounts`, `payments`, and `invoices` for ticket 102 and payment decisions.

Run from the project root with `python -m mcp_server.server` after installing requirements.

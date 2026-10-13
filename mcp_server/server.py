"""Campus Customs MCP tools. All shop facts come from the working SQLite DB."""
from pathlib import Path
import json, sqlite3

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "campus_customs_new.db"

def query(sql, params=()):
    with sqlite3.connect(DB_PATH) as db:
        db.row_factory = sqlite3.Row
        return [dict(r) for r in db.execute(sql, params).fetchall()]

def ticket_context(ticket_id: int):
    return query("SELECT * FROM tickets WHERE id=?", (ticket_id,))

def check_stock_and_price(ticket_id: int):
    """Tool for customer orders or discount requests (tickets 101 and 103)."""
    t = ticket_context(ticket_id)
    if not t or not t[0]["sku"]:
        return {"ticket_id": ticket_id, "ticket": t, "message": "No SKU-based request"}
    sku, size = t[0]["sku"], t[0]["size"]
    return {"ticket_id": ticket_id, "ticket": t[0],
            "inventory": query("SELECT * FROM inventory WHERE sku=? AND size=?", (sku, size)),
            "pricing": query("SELECT * FROM pricing WHERE sku=?", (sku,))}

def check_vendor_invoice_and_restock(ticket_id: int):
    """Tool for deciding whether a stock shortfall can be restocked (ticket 101/103)."""
    t = ticket_context(ticket_id)
    if not t or not t[0]["sku"]:
        return {"ticket_id": ticket_id, "message": "No SKU-based request"}
    return {"ticket_id": ticket_id, "ticket": t[0],
            "vendors": query("SELECT * FROM vendors"),
            "open_invoices": query("SELECT * FROM invoices WHERE status!='paid'"),
            "pricing": query("SELECT * FROM pricing WHERE sku=?", (t[0]["sku"],))}

def check_lease_and_cash(ticket_id: int):
    """Tool for rent and payment decisions (ticket 102, plus safe approval context)."""
    return {"ticket_id": ticket_id,
            "today": query("SELECT date_today FROM desk")[0]["date_today"],
            "leases": query("SELECT * FROM leases"),
            "cash": query("SELECT * FROM cash_accounts"),
            "payments": query("SELECT * FROM payments"),
            "invoices": query("SELECT * FROM invoices")}

try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("campus-customs")
    mcp.tool()(check_stock_and_price)
    mcp.tool()(check_vendor_invoice_and_restock)
    mcp.tool()(check_lease_and_cash)
except ImportError:
    mcp = None

if __name__ == "__main__":
    if mcp is None:
        raise SystemExit("Install requirements.txt to run the MCP server")
    mcp.run()

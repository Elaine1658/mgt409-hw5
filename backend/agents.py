from pathlib import Path
import sqlite3, json
import asyncio
from mcp_server.server import check_stock_and_price, check_vendor_invoice_and_restock, check_lease_and_cash
from .ai_config import MODEL_NAME
from .pydantic_team import run_live_ticket

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "campus_customs_new.db"
PROMPTS = ROOT / "backend" / "prompts"

def run_ticket(ticket_id: int):
    live_result = asyncio.run(run_live_ticket(ticket_id))
    if live_result is not None:
        with sqlite3.connect(DB) as db:
            db.execute("UPDATE tickets SET status=? WHERE id=?", (live_result['status'], ticket_id)); db.commit()
        return live_result
    with sqlite3.connect(DB) as db:
        db.row_factory = sqlite3.Row
        t = dict(db.execute("SELECT * FROM tickets WHERE id=?", (ticket_id,)).fetchone())
    events=[]; proposals=[]
    def msg(agent,text,kind="message",tool=None):
        events.append({"ticket_id":ticket_id,"agent":agent,"kind":kind,"text":text,"tool":tool})
    msg("Boss", f"I am reviewing ticket {ticket_id}: {t['subject']}.")
    if t["type"] == "rent_notice":
        facts=check_lease_and_cash(ticket_id); msg("Boss","Delegating lease timing to Facilities.","handoff")
        msg("Facilities", "Checked the lease, shop date, cash and payment history.","tool","check_lease_and_cash")
        lease=facts["leases"][0]; due=lease["next_due"]
        msg("Facilities",f"Rent of ${lease['monthly_rent']:.2f} is due {due}; I prepared a human approval request.")
        proposals.append({"kind":"rent","amount":lease["monthly_rent"],"ref_id":lease["id"],"reason":"Monthly shop rent"})
    else:
        facts=check_stock_and_price(ticket_id); msg("Boss","Delegating stock and price checking to Inventory.","handoff")
        msg("Inventory","Checked requested SKU and size against current stock and pricing.","tool","check_stock_and_price")
        inv=(facts.get("inventory") or [{}])[0]; qty=t["qty"] or 0
        if inv.get("qty",0) >= qty:
            msg("Inventory",f"There is enough stock ({inv['qty']} available for {qty} requested).")
        else:
            shortage=qty-inv.get("qty",0); restock=check_vendor_invoice_and_restock(ticket_id)
            msg("Inventory",f"There is a shortfall of {shortage}; checked vendors and unpaid invoices.","tool","check_vendor_invoice_and_restock")
            blocked=bool(restock.get("open_invoices"))
            msg("Boss", "Restock is blocked by an open unpaid vendor invoice." if blocked else "Restock can be planned using the vendor lead time.")
        price=(facts.get("pricing") or [{}])[0]
        if t["type"] == "price_override":
            msg("Accounting",f"List price is ${price.get('list_price',0):.2f}; margin review is required before any discount.")
    status = 'awaiting_approval' if proposals else 'resolved'
    with sqlite3.connect(DB) as db:
        db.execute("UPDATE tickets SET status=? WHERE id=?",(status, ticket_id)); db.commit()
    return {"ticket_id":ticket_id,"status":status,"events":events,"proposals":proposals,
            "summary":f"Resolved by Boss with one specialist handoff; {len(events)} events recorded."}

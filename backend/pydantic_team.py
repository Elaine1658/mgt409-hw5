"""The live PydanticAI team used when LIVE_AI=true and a Portkey key exists."""
from dataclasses import dataclass, field
from typing import Any
from pydantic import BaseModel
from pydantic_ai import RunContext

from .ai_config import make_pydantic_agent
from .models import AgentEvent
from mcp_server.server import check_stock_and_price, check_vendor_invoice_and_restock, check_lease_and_cash

class BossDecision(BaseModel):
    summary: str
    resolved: bool
    payment_amount: float | None = None
    payment_kind: str | None = None
    payment_ref_id: int | None = None

@dataclass
class TeamDeps:
    ticket_id: int
    events: list[dict[str, Any]] = field(default_factory=list)
    depth: int = 0

def _event(ctx: RunContext[TeamDeps], agent: str, text: str, kind: str='message', tool: str|None=None):
    ctx.deps.events.append({'ticket_id':ctx.deps.ticket_id,'agent':agent,'kind':kind,'text':text,'tool':tool})

def build_team():
    prompts = {
        'boss': 'You are Boss. Review the ticket, use MCP tools, delegate to one specialist, and make a final decision. Never invent shop facts. Payments are only proposals for human approval.',
        'inventory': 'You are Inventory. Check SKU, size, stock, vendor lead time, and unpaid invoices through MCP. Never contact vendors or change the database.',
        'accounting': 'You are Accounting. Check cash, invoices, costs, and margins through MCP. Prepare payment proposals only; a human must approve payments and cash cannot go negative.',
        'facilities': 'You are Facilities. Check leases and due dates through MCP. Prepare rent recommendations but never pay or contact the landlord.',
        'customer_service': 'You are Customer Service. Draft a polite customer response from MCP-backed facts. Never send email or promise unsupported facts.',
    }
    boss = make_pydantic_agent(prompts['boss'], name='boss', output_type=BossDecision, deps_type=TeamDeps)
    specialists = {role: make_pydantic_agent(prompt, name=role, deps_type=TeamDeps) for role, prompt in prompts.items() if role != 'boss'}
    if boss is None or any(x is None for x in specialists.values()):
        return None

    def stock(ctx: RunContext[TeamDeps]):
        _event(ctx, 'Inventory', 'Called MCP stock and pricing tool.', 'tool', 'check_stock_and_price')
        return check_stock_and_price(ctx.deps.ticket_id)
    def vendor(ctx: RunContext[TeamDeps]):
        _event(ctx, 'Inventory', 'Called MCP vendor and invoice tool.', 'tool', 'check_vendor_invoice_and_restock')
        return check_vendor_invoice_and_restock(ctx.deps.ticket_id)
    def lease(ctx: RunContext[TeamDeps]):
        _event(ctx, 'Facilities', 'Called MCP lease and cash tool.', 'tool', 'check_lease_and_cash')
        return check_lease_and_cash(ctx.deps.ticket_id)
    def delegate(ctx: RunContext[TeamDeps], role: str, task: str):
        if role not in specialists or ctx.deps.depth >= 2:
            return 'Delegation refused: choose an available specialist and keep the handoff short.'
        _event(ctx, 'Boss', f'Delegating to {role}: {task}', 'handoff')
        child = TeamDeps(ctx.deps.ticket_id, ctx.deps.events, ctx.deps.depth + 1)
        result = specialists[role].run_sync(task, deps=child)
        _event(ctx, role, str(result.output))
        return result.output
    for agent in [boss, *specialists.values()]:
        agent.tool(stock)
        agent.tool(vendor)
        agent.tool(lease)
        agent.tool(delegate)
    return {'boss': boss, **specialists}

def run_live_ticket(ticket_id: int):
    team = build_team()
    if team is None:
        return None
    deps = TeamDeps(ticket_id)
    result = team['boss'].run_sync(f'Review and resolve ticket {ticket_id}. Use MCP facts, delegate to the best specialist, and return a concise final decision.', deps=deps)
    deps.events.insert(0, {'ticket_id':ticket_id,'agent':'Boss','kind':'message','text':'Live PydanticAI Boss run started.','tool':None})
    decision = result.output
    proposals=[]
    if decision.payment_amount:
        proposals.append({'kind':decision.payment_kind or 'payment','amount':decision.payment_amount,'ref_id':decision.payment_ref_id,'reason':decision.summary})
    return {'ticket_id':ticket_id,'status':'resolved' if decision.resolved else 'open','events':deps.events,'proposals':proposals,'summary':decision.summary}

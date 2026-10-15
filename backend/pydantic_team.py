"""The live PydanticAI team used when LIVE_AI=true and a Portkey key exists."""
from dataclasses import dataclass, field
from typing import Any
from pathlib import Path
import sqlite3
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

class SpecialistDecision(BaseModel):
    summary: str
    resolved: bool = False
    payment_amount: float | None = None
    payment_kind: str | None = None
    payment_ref_id: int | None = None

@dataclass
class TeamDeps:
    ticket_id: int
    events: list[dict[str, Any]] = field(default_factory=list)
    depth: int = 0
    actor: str = 'Boss'
    payment_fields: dict[str, Any] = field(default_factory=dict)

def _event(ctx: RunContext[TeamDeps], agent: str, text: str, kind: str='message', tool: str|None=None):
    ctx.deps.events.append({'ticket_id':ctx.deps.ticket_id,'agent':agent,'kind':kind,'text':text,'tool':tool})

def _first_specialist_for_ticket(ticket_id: int) -> str | None:
    """Apply the prompt's routing policy from the ticket type, never ticket ids."""
    from .agents import DB
    with sqlite3.connect(DB) as db:
        row = db.execute('SELECT type FROM tickets WHERE id=?', (ticket_id,)).fetchone()
    return {'customer_order': 'inventory', 'price_override': 'inventory',
            'rent_notice': 'facilities'}.get(row[0]) if row else None

def build_team():
    prompt_dir = Path(__file__).resolve().parent / 'prompts'
    prompts = {role: (prompt_dir / f'{role}.md').read_text(encoding='utf-8') for role in
               ('boss', 'inventory', 'accounting', 'facilities', 'customer_service')}
    boss = make_pydantic_agent(prompts['boss'], name='boss', output_type=BossDecision, deps_type=TeamDeps)
    specialists = {role: make_pydantic_agent(prompt, name=role, output_type=SpecialistDecision, deps_type=TeamDeps) for role, prompt in prompts.items() if role != 'boss'}
    if boss is None or any(x is None for x in specialists.values()):
        return None

    def stock(ctx: RunContext[TeamDeps]):
        _event(ctx, ctx.deps.actor, 'Called MCP stock and pricing tool.', 'tool', 'check_stock_and_price')
        return check_stock_and_price(ctx.deps.ticket_id)
    def vendor(ctx: RunContext[TeamDeps]):
        _event(ctx, ctx.deps.actor, 'Called MCP vendor and invoice tool.', 'tool', 'check_vendor_invoice_and_restock')
        return check_vendor_invoice_and_restock(ctx.deps.ticket_id)
    def lease(ctx: RunContext[TeamDeps]):
        _event(ctx, ctx.deps.actor, 'Called MCP lease and cash tool.', 'tool', 'check_lease_and_cash')
        return check_lease_and_cash(ctx.deps.ticket_id)
    async def delegate(ctx: RunContext[TeamDeps], role: str, task: str):
        requested_role = role.strip().lower().replace(' ', '_')
        if requested_role not in specialists or ctx.deps.depth >= 2:
            return 'Delegation refused: choose an available specialist and keep the handoff short.'
        first_role = _first_specialist_for_ticket(ctx.deps.ticket_id)
        if ctx.deps.depth == 0 and first_role and requested_role != first_role:
            return f'Delegation refused: follow the Boss routing policy and hand this ticket first to {first_role}.'
        label = requested_role.replace('_', ' ').title()
        _event(ctx, ctx.deps.actor,
               f'Delegating to {label}: {task}', 'handoff')
        child = TeamDeps(ctx.deps.ticket_id, ctx.deps.events, ctx.deps.depth + 1, label)
        result = await specialists[requested_role].run(task, deps=child)
        specialist_output = result.output
        if isinstance(specialist_output, SpecialistDecision) and specialist_output.payment_amount:
            ctx.deps.payment_fields = {
                'amount': specialist_output.payment_amount,
                'kind': specialist_output.payment_kind or 'payment',
                'ref_id': specialist_output.payment_ref_id,
                'reason': specialist_output.summary,
            }
        _event(ctx, label, str(result.output))
        return specialist_output

    # Keep the Boss's action surface narrow so a live run must show a real
    # Boss -> specialist handoff instead of letting Boss do all MCP work.
    boss.tool(delegate)
    for role, agent in specialists.items():
        agent.tool(delegate)
        if role == 'inventory':
            agent.tool(stock)
            agent.tool(vendor)
        elif role == 'facilities':
            agent.tool(lease)
        elif role == 'accounting':
            agent.tool(stock)
            agent.tool(vendor)
            agent.tool(lease)
    return {'boss': boss, **specialists}

async def run_live_ticket(ticket_id: int):
    team = build_team()
    if team is None:
        return None
    deps = TeamDeps(ticket_id)
    result = await team['boss'].run(f'Review and resolve ticket {ticket_id}. Use MCP facts, delegate to the best specialist, and return a concise final decision.', deps=deps)
    deps.events.insert(0, {'ticket_id':ticket_id,'agent':'Boss','kind':'message','text':'Live PydanticAI Boss run started.','tool':None})
    decision = result.output
    proposals=[]
    if decision.payment_amount:
        proposals.append({'kind':decision.payment_kind or 'payment','amount':decision.payment_amount,'ref_id':decision.payment_ref_id,'reason':decision.summary})
    elif deps.payment_fields:
        proposals.append({'kind': deps.payment_fields['kind'], 'amount': deps.payment_fields['amount'],
                          'ref_id': deps.payment_fields['ref_id'], 'reason': deps.payment_fields['reason']})
    status = 'awaiting_approval' if proposals else ('resolved' if decision.resolved else 'open')
    return {'ticket_id':ticket_id,'status':status,'events':deps.events,'proposals':proposals,'summary':decision.summary}

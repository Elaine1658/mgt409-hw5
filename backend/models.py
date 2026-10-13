from typing import Literal, Optional
from pydantic import BaseModel

class Ticket(BaseModel):
    id: int
    type: str
    requester: str
    subject: str
    status: str
    notes: Optional[str] = None

class AgentEvent(BaseModel):
    ticket_id: int
    agent: str
    kind: Literal["message", "tool", "handoff", "approval"]
    text: str
    tool: Optional[str] = None

class ApprovalRequest(BaseModel):
    ticket_id: int
    amount: float
    kind: str = "rent"
    ref_id: Optional[int] = None
    approved_by: str

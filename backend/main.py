from pathlib import Path
import json, shutil, sqlite3, time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .agents import run_ticket, DB, ROOT
from .models import ApprovalRequest

ORIGINAL=ROOT/'data'/'campus_customs.db'
AUDIT=ROOT/'output'/'audit_trail.json'
app=FastAPI(title='Campus Customs Operations API')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
EVENTS=[]; RESULTS={}

def rows(sql,args=()):
    with sqlite3.connect(DB) as db:
        db.row_factory=sqlite3.Row
        return [dict(r) for r in db.execute(sql,args).fetchall()]
def append_audit(new_events):
    AUDIT.parent.mkdir(exist_ok=True)
    try:
        history=json.loads(AUDIT.read_text(encoding='utf-8'))
        if not isinstance(history, list): history=[]
    except (FileNotFoundError, json.JSONDecodeError):
        history=[]
    history.extend(new_events)
    AUDIT.write_text(json.dumps(history,indent=2), encoding='utf-8')

@app.get('/api/tickets')
def tickets(): return rows('SELECT * FROM tickets ORDER BY id')
@app.post('/api/tickets/{ticket_id}/run')
def run(ticket_id:int):
    if not rows('SELECT * FROM tickets WHERE id=?',(ticket_id,)): raise HTTPException(404,'Ticket not found')
    result=run_ticket(ticket_id); RESULTS[ticket_id]=result; EVENTS.extend(result['events']); append_audit(result['events']); return result
@app.get('/api/events')
def events(): return EVENTS
@app.get('/api/cash')
def cash(): return rows("SELECT * FROM cash_accounts WHERE name='checking'")[0]
@app.post('/api/approve-pay')
def approve_pay(req:ApprovalRequest):
    account=cash(); amount=float(req.amount)
    if amount<=0 or amount>account['balance']: raise HTTPException(400,'Payment refused: insufficient cash or invalid amount')
    with sqlite3.connect(DB) as db:
        now=rows('SELECT date_today FROM desk')[0]['date_today']
        db.execute('UPDATE cash_accounts SET balance=balance-? WHERE name=?',(amount,'checking'))
        db.execute('INSERT INTO payments(kind,ref_id,amount,account,paid_at,approved_by) VALUES(?,?,?,?,?,?)',(req.kind,req.ref_id,amount,'checking',now,req.approved_by)); db.commit()
    event={'ticket_id':req.ticket_id,'agent':'Human approval','kind':'approval','text':f'Approved ${amount:.2f} for {req.kind} by {req.approved_by}'}
    EVENTS.append(event); append_audit([event]); return {'ok':True,'cash':cash(),'event':event}
@app.post('/api/reset')
def reset():
    shutil.copyfile(ORIGINAL,DB); EVENTS.clear(); RESULTS.clear()
    append_audit([{'agent':'System','kind':'reset','text':'Working database reset from the untouched original.','tool':None}])
    return {'ok':True,'cash':cash()}
@app.get('/api/results/{ticket_id}')
def result(ticket_id:int): return RESULTS.get(ticket_id, {'status':'not_run'})

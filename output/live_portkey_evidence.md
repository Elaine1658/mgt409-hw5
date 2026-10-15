# Live Portkey verification

The final clean verification was run on 2026-10-14 with `LIVE_AI=true` and the locally configured course key. The key was not printed, committed, or written to an output file.

- Model: `gpt-6-luna`
- Provider endpoint: Portkey `/v1/chat/completions`
- Tickets tested: 101, 102, and 103
- Result: Portkey returned HTTP 200 responses for the final clean run.
- Delegation observed: 101 Boss → Inventory → Customer Service; 102 Boss → Facilities; 103 Boss → Inventory → Customer Service. The Expected plan intentionally records the original Accounting handoff expectation so P10 can discuss the difference.
- Safety result: 101 and 103 stayed open because fulfillment was unsupported; 102 produced a $2,400 proposal and stayed pending until human approval.
- Approval result: the local human approval route recorded a $2,400 rent payment and changed checking cash from $3,400 to $1,000.
- The $2,400 proposal in the final run came from Facilities' structured `SpecialistDecision` fields and was propagated through the delegation result; there is no ticket-id-specific payment fallback in the code.

The repository still supports an offline deterministic path when `LIVE_AI` is not enabled or no key is present. This evidence records the real live check without exposing the credential.

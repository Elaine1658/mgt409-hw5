# Live Portkey verification

Manual verification was run on 2026-10-14 with `LIVE_AI=true` and the locally configured course key. The key was not printed, committed, or written to an output file.

- Model: `gpt-6-luna`
- Provider endpoint: Portkey `/v1/chat/completions`
- Ticket tested: 101
- Result: Portkey returned HTTP 200 responses and the workflow completed with status `open` because the tee is unavailable.
- Delegation observed: Boss → Inventory → Accounting.
- Safety result: the open vendor invoice blocked fulfillment; no payment was made.

The repository still supports an offline deterministic path when `LIVE_AI` is not enabled or no key is present. This evidence records the real live check without exposing the credential.

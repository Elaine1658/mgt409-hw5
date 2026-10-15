# Dashboard design

The board is designed as a small campus-shop operations desk rather than a default Vite page. A warm paper background keeps the page approachable, teal is used for trusted system state and cash, and amber marks the main operator action. The left rail makes the three tickets easy to scan and keeps the selected ticket visible while the right panel shows the decision trail.

The live view has four layers: ticket status, a per-agent summary showing update/tool counts, the detailed event stream, and a desk summary with a human approval action when money is proposed. The board refreshes tickets, cash, and events from the FastAPI routes. The static `desk_tickets.html` report mirrors the same operational concepts with Expected, Actual, Cash, and Reflection tabs so the grader can inspect the clean-run evidence without starting the app.

"""Protocol-level MCP smoke test for Problem 4.

Run from the project root. It starts the local stdio server, initializes an
MCP client, discovers all three tools, calls each one, and saves short results.
"""
import asyncio, json, subprocess
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output' / 'mcp_smoke.json'

async def main():
    params = StdioServerParameters(command='python3', args=['-m', 'mcp_server.server'], cwd=str(ROOT))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            discovered = await session.list_tools()
            requests = [
                ('Check the tee stock and price for ticket 101', 'check_stock_and_price', {'ticket_id': 101}),
                ('Check vendor restock constraints for ticket 101', 'check_vendor_invoice_and_restock', {'ticket_id': 101}),
                ('Check rent and cash for ticket 102', 'check_lease_and_cash', {'ticket_id': 102}),
            ]
            output=[]
            names={tool.name for tool in discovered.tools}
            for prompt, name, args in requests:
                if name not in names: raise RuntimeError(f'Missing MCP tool: {name}')
                result=await session.call_tool(name, args)
                text=getattr(result.content[0], 'text', '') if result.content else ''
                output.append({'prompt':prompt,'tool':name,'short_output':text[:500]})
    OUT.write_text(json.dumps(output, indent=2), encoding='utf-8')
    print(f'Wrote {OUT}')

if __name__ == '__main__': asyncio.run(main())

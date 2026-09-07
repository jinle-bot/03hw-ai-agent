from langchain_mcp_adapters.client import MultiServerMCPClient

from agent.config import MCP_SERVER_URL


def create_mcp_client() -> MultiServerMCPClient:
    return MultiServerMCPClient(
        {
            "school": {
                "transport": "http",
                "url": MCP_SERVER_URL,
            },

            "thinking": {
                "transport": "stdio",
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-sequential-thinking",
                ],
            },

        },
        tool_name_prefix=True,
    )

async def load_tools():
    client = create_mcp_client()
    tools = await client.get_tools()

    return tools
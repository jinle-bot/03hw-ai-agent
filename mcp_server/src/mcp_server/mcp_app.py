from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings


server = FastMCP(
    name="mcp_server",
    host="0.0.0.0",
    port=8000,
    stateless_http=True,
    json_response=True,
    transport_security=TransportSecuritySettings(
        allowed_hosts=[
            "localhost:*",
            "127.0.0.1:*",
            "mcp-server:*",
        ],
    ),
)
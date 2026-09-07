from starlette.responses import JSONResponse
from starlette.routing import Route

from mcp_server import tool
from mcp_server.mcp_app import server


async def health(request):
    return JSONResponse({"status": "ok"})


api = server.streamable_http_app()

api.routes.append(
    Route("/health", health, methods=["GET"])
)

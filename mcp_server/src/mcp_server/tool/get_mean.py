from typing import Literal

from pydantic import BaseModel

from mcp_server.mcp_app import server
from mcp_server.tool.data import DATA


class MeanRes(BaseModel):
    status: Literal["found", "not_found"]
    mean: float | None = None
    message: str | None = None


@server.tool()
def get_mean() -> MeanRes:
    """Vrací průměr ze všech zapsaných předmětů."""
    if not DATA:
        return MeanRes(
            status="not_found",
            message="Žádné předměty tu nejsou"
        )
    return MeanRes(
        status="found",
        mean=sum(DATA.values()) / len(DATA)
    )

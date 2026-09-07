from typing import Literal

from pydantic import BaseModel, Field

from mcp_server.mcp_app import server

from mcp_server.tool.data import DATA


class GradeRes(BaseModel):
    status: Literal["found", "not_found"]
    grade: int | None = None
    message: str | None = None


@server.tool()
async def get_grade(name: str = Field(description="Jméno předmětu")) -> GradeRes:
    """Vrátí známku z předmětu, případně informaci, že předmět není zapsaný."""
    grade = DATA.get(name.lower())
    if grade is None:
        return GradeRes(
            status="not_found",
            message=f"Předmět {name} nemáš zapsaný"
        )
    return GradeRes(
        status="found",
        grade=grade,
    )
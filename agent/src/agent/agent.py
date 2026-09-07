from langchain.agents import create_agent

from agent.mcp import load_tools
from agent.model import create_model


async def create_school_agent():
    tools = await load_tools()
    model = create_model()

    return create_agent(
        model=model,
        tools=tools,
        system_prompt=(
            "You are a helpful AI assistant with access to external tools. "
            "Use the school tools whenever the user asks about grades, subjects, "
            "or other school-related data. Never invent school data if a tool "
            "can provide the answer. "
            "Use the sequential-thinking tool for complex tasks that benefit from "
            "step-by-step analysis, planning, comparison, or decomposition. "
            "For simple questions, answer directly without using tools unnecessarily."
        ),
    )

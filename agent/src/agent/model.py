from langchain_openai import ChatOpenAI


def create_model() -> ChatOpenAI:
    return ChatOpenAI(
        model="gpt-5-nano",
        temperature=0,
    )
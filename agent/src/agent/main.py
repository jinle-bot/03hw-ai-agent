import asyncio

from agent.agent import create_school_agent


async def async_main() -> None:
    agent = await create_school_agent()

    messages = []

    print("Agent is ready.")
    print("Type 'exit' or 'quit' to terminate.\n")

    while True:
        print("=" * 50)
        user_input = await asyncio.to_thread(input, "You: ")

        if user_input.strip().lower() in {"exit", "quit"}:
            print("Exiting.")
            break

        if not user_input.strip():
            continue

        messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        response = await agent.ainvoke(
            {
                "messages": messages,
            }
        )

        assistant_message = response["messages"][-1]

        print("=" * 50)
        print(f"\nAgent: {assistant_message.content}\n")

        messages.append(
            {
                "role": "assistant",
                "content": assistant_message.content,
            }
        )


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
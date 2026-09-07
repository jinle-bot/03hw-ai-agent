import uvicorn


def main() -> None:
    print("Hello from mcp-server!")
    uvicorn.run(
        "mcp_server.starlette_app:api",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        workers=1,
    )


if __name__ == "__main__":
    main()

import asyncio

from fastmcp import FastMCP

from agent.mcp.servers import io

main_mcp = FastMCP(name="MainApp")


async def serve_main_mcp():
    await main_mcp.import_server(io.mcp)


if __name__ == "__main__":
    asyncio.run(serve_main_mcp())
    main_mcp.run(transport="stdio")

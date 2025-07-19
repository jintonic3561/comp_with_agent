import asyncio

from fastmcp import FastMCP

from agent.mcp.servers import data_information, function_executor, notebook_writer

main_mcp = FastMCP(name="MainApp")


async def serve_main_mcp():
    await main_mcp.import_server(data_information.mcp)
    await main_mcp.import_server(function_executor.mcp)
    await main_mcp.import_server(notebook_writer.mcp)


if __name__ == "__main__":
    asyncio.run(serve_main_mcp())
    main_mcp.run(transport="stdio")

from fastmcp import FastMCP

mcp = FastMCP("Data IO Server")

# Register resources and tools in our main server
# mcp.tool(load_data)


if __name__ == "__main__":
    mcp.run(transport="stdio")

from fastmcp import FastMCP

from agent.mcp.components.notebook_writer.tools import add_cell_to_notebook

mcp = FastMCP("Notebook Writer Server")

mcp.tool(add_cell_to_notebook)

if __name__ == "__main__":
    mcp.run(transport="stdio")

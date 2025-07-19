from fastmcp import FastMCP

from agent.mcp.components.data_information.tools import (
    get_data_description,
    get_join_keys_info,
    get_problem_formulation,
    list_available_data,
)

mcp = FastMCP("Data Information Server")

mcp.tool(get_data_description)
mcp.tool(get_join_keys_info)
mcp.tool(get_problem_formulation)
mcp.tool(list_available_data)

if __name__ == "__main__":
    mcp.run(transport="stdio")

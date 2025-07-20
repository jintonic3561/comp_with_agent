from fastmcp import FastMCP

from agent.mcp.components.analysis_executor.tools import (
    execute_all_data_analysis,
    execute_soil_analysis,
    execute_timeseries_analysis,
)

mcp = FastMCP("analysis_executor")

mcp.tool(execute_all_data_analysis)
mcp.tool(execute_soil_analysis)
mcp.tool(execute_timeseries_analysis)

if __name__ == "__main__":
    mcp.run(transport="stdio")

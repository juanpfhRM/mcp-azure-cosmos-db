import logging
import os
import sys

from semantic_kernel.connectors.mcp import MCPStdioPlugin

mcp_log_analytics_plugin = None

async def init_mcp_log_analytics_plugin():
    global mcp_log_analytics_plugin

    if mcp_log_analytics_plugin:
        return mcp_log_analytics_plugin
    try:
        mcp_log_analytics_plugin = MCPStdioPlugin(
            name="AzureLogAnalyticsTools",
            description="Azure Log Analytics Query Tools",
            command="node",
            args=["src/plugins/mcp/logAnalytics/js/index.js"],
            env={
                "LOG_ANALYTICS_WORKSPACE_ID": os.getenv("LOG_ANALYTICS_WORKSPACE_ID")
            }
        )
        await mcp_log_analytics_plugin.__aenter__()

        logging.info(f"[MCPLogAnalyticsPlugin] mcp_log_analytics_plugin generado correctamente.")
        return mcp_log_analytics_plugin
    except Exception as e:
        logging.error(f"[MCPLogAnalyticsPlugin] Error: No fue posible generar mcp_log_analytics_plugin. {str(e)}")
        sys.exit(1)

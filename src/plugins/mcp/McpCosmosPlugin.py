# app\src\plugins\mcp\McpCosmosPlugin.py
import logging
import os

from semantic_kernel.connectors.mcp import MCPStdioPlugin

mcp_cosmos_plugin = None

async def init_mcp_cosmos_plugin():
    global mcp_cosmos_plugin

    try:
        mcp_cosmos_plugin = MCPStdioPlugin(
            name="AzureCosmosDBTools",
            description="Azure Cosmos DB Management Tools",
            command="node",
            args=["src/plugins/mcp/js/index.js"],
            env={
                "COSMOSDB_URI": os.getenv("COSMOSDB_URI"),
                "COSMOSDB_KEY": os.getenv("COSMOSDB_KEY"),
                "COSMOS_DATABASE_ID": os.getenv("COSMOS_DATABASE_ID"),
                "COSMOS_CONTAINER_ID": os.getenv("COSMOS_CONTAINER_ID")
            }
        )
        await mcp_cosmos_plugin.__aenter__()

        logging.info(f"[MCPCosmosPlugin] mcp_cosmos_plugin generado correctamente.")
        return mcp_cosmos_plugin
    except Exception as e:
        logging.error(f"[MCPCosmosPlugin] Error: No fue posible generar mcp_cosmos_plugin. {str(e)}")
        return None

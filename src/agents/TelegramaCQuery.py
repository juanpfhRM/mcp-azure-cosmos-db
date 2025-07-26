import logging
import os
import sys

from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.functions import KernelArguments

from src.models.CosmosSqlQuery import CosmosSqlQueryResult
from src.plugins.CodificarTelegramaPlugin import CodificarTelegramaPlugin
from src.plugins.FechaPlugin import FechaPlugin
from src.plugins.mcp.cosmos import McpCosmosPlugin
from src.utils.Metaprompts import metaprompt_telegramacquery_agent

async def init_agent_telegramacquery():
    try:
        
        chat_service = AzureChatCompletion(
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        )

        mcp_cosmos_plugin = await McpCosmosPlugin.init_mcp_cosmos_plugin()

        execution_settings = OpenAIChatPromptExecutionSettings()
        execution_settings.response_format = CosmosSqlQueryResult

        agent_telegramacquery= ChatCompletionAgent(
            service=chat_service,
            name="TelegramaCQuery",
            instructions=metaprompt_telegramacquery_agent.substitute(
                database=os.getenv("COSMOS_DATABASE_ID", "cambrica_db"),
                container=os.getenv("COSMOS_CONTAINER_ID", "history")
            ),
            plugins=[mcp_cosmos_plugin, CodificarTelegramaPlugin(), FechaPlugin()],
            arguments=KernelArguments(settings=execution_settings)
        )

        logging.info(f"[TelegramaCQuery] agent_telegramacquery generado correctamente.")
        return agent_telegramacquery
    except Exception as e:
        logging.error(f"[TelegramaCQuery] Error: No fue posible generar agent_telegramacquery. {str(e)}")
        sys.exit(1)

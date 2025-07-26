import logging
import os
import sys

from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.functions import KernelArguments

from src.models.LogAnalyticsKqlQuery import LogAnalyticsKqlQueryResult
from src.plugins.CodificarTelegramaPlugin import CodificarTelegramaPlugin
from src.plugins.FechaPlugin import FechaPlugin
from src.plugins.mcp.logAnalytics import McpLogAnalyticsPlugin
from src.utils.Metaprompts import metaprompt_telegramakquery_agent

async def init_agent_telegramakquery():
    try:
        
        chat_service = AzureChatCompletion(
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        )

        mcp_log_analytics_plugin = await McpLogAnalyticsPlugin.init_mcp_log_analytics_plugin()

        execution_settings = OpenAIChatPromptExecutionSettings()
        execution_settings.response_format = LogAnalyticsKqlQueryResult

        agent_telegramakquery = ChatCompletionAgent(
            service=chat_service,
            name="TelegramaKQuery",
            instructions=metaprompt_telegramakquery_agent.substitute(
                database=os.getenv("COSMOS_DATABASE_ID", "cambrica_db"),
                container=os.getenv("COSMOS_CONTAINER_ID", "history")
            ),
            plugins=[mcp_log_analytics_plugin, CodificarTelegramaPlugin(), FechaPlugin()],
            arguments=KernelArguments(settings=execution_settings)
        )

        logging.info(f"[TelegramaKQuery] agent_telegramakquery generado correctamente.")
        return agent_telegramakquery
    except Exception as e:
        logging.error(f"[TelegramaKQuery] Error: No fue posible generar agent_telegramakquery. {str(e)}")
        sys.exit(1)

import logging
import os
import sys

from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.functions import KernelArguments

from src.models.LogAnalyticsKqlQuery import LogAnalyticsKqlQuery
from src.plugins.CodificarTelegramaPlugin import CodificarTelegramaPlugin
from src.plugins.FechaPlugin import FechaPlugin
from src.utils.Metaprompts import metaprompt_telegramakquery_csv_agent

async def init_agent_telegramakquery_csv():
    try:
        
        chat_service = AzureChatCompletion(
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        )

        execution_settings = OpenAIChatPromptExecutionSettings()
        execution_settings.response_format = LogAnalyticsKqlQuery

        agent_telegramacquery_csv= ChatCompletionAgent(
            service=chat_service,
            name="TelegramaCQueryCSV",
            instructions=metaprompt_telegramakquery_csv_agent.substitute(
                database=os.getenv("COSMOS_DATABASE_ID", "cambrica_db"),
                container=os.getenv("COSMOS_CONTAINER_ID", "history")
            ),
            plugins=[CodificarTelegramaPlugin(), FechaPlugin()],
            arguments=KernelArguments(settings=execution_settings)
        )

        logging.info(f"[TelegramaKQueryCSV] agent_telegramakquery_csv generado correctamente.")
        return agent_telegramacquery_csv
    except Exception as e:
        logging.error(f"[TelegramaKQueryCSV] Error: No fue posible generar agent_telegramakquery_csv. {str(e)}")
        sys.exit(1)

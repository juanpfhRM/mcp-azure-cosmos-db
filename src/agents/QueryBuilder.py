# src\agents\QueryBuilder.py
import logging
import os

from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.functions import KernelArguments

from src.models.CosmosSqlQuery import CosmosSqlQuery
from src.plugins.CodificarTelegramaPlugin import CodificarTelegramaPlugin
from src.plugins.FechaPlugin import FechaPlugin
from src.utils.Metaprompts import metaprompt_querybuilder_agent

async def init_agent_querybuilder():
    try:
        
        chat_service = AzureChatCompletion(
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        )

        execution_settings = OpenAIChatPromptExecutionSettings()
        execution_settings.response_format = CosmosSqlQuery

        agent_querybuilder = ChatCompletionAgent(
            service=chat_service,
            name="QueryBuilder",
            instructions=metaprompt_querybuilder_agent.substitute(
                database=os.getenv("COSMOS_DATABASE_ID", "cambrica_db"),
                container=os.getenv("COSMOS_CONTAINER_ID", "history")
            ),
            plugins=[CodificarTelegramaPlugin(), FechaPlugin()],
            arguments=KernelArguments(settings=execution_settings)
        )

        logging.info(f"[QueryBuilder] agent_querybuilder generado correctamente.")
        return agent_querybuilder
    except Exception as e:
        logging.error(f"[QueryBuilder] Error: No fue posible generar agent_querybuilder. {str(e)}")
        return None

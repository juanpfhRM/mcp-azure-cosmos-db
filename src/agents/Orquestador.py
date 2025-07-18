import logging
import os
import sys

from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.functions import KernelArguments

from src.plugins.DecodificarTelegramaPlugin import DecodificarTelegramaPlugin
from src.models.ChatResponse import ChatResponse
from src.utils.Metaprompts import metaprompt_orquestador_agent
from src.plugins import init_reportequery_plugin, init_telegramaquery_plugin, init_telegramaquery_csv_plugin

agent_orquestador = None

async def init_agent_orquestador():
    try:
        chat_service = AzureChatCompletion(
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        )

        execution_settings = OpenAIChatPromptExecutionSettings()
        execution_settings.response_format = ChatResponse

        agent_reportquery_plugin = await init_reportequery_plugin()
        agent_telegramaquery_plugin = await init_telegramaquery_plugin()
        agent_telegramaquery_csv_plugin = await init_telegramaquery_csv_plugin()

        agent_orquestador = ChatCompletionAgent(
            service=chat_service,
            name="OrquestadorAssistant",
            instructions=metaprompt_orquestador_agent.substitute(
                umbral_telegramas=os.getenv("UMBRAL_TELEGRAMAS", "3")
            ),
            plugins=[DecodificarTelegramaPlugin(), agent_reportquery_plugin, agent_telegramaquery_plugin, agent_telegramaquery_csv_plugin],
            arguments=KernelArguments(settings=execution_settings)
        )
        logging.info(f"[Orquestador] agent_orquestador generado correctamente.")
        return agent_orquestador
    except Exception as e:
        logging.error(f"[Orquestador] Error: No fue posible generar agent_orquestador. {str(e)}")
        sys.exit(1)

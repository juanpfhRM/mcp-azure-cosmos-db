import logging
import os

from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

from src.plugins.mcp import McpCosmosPlugin
from src.plugins.DecodificarTelegramaPlugin import DecodificarTelegramaPlugin
from src.utils.Metaprompts import metaprompt_orquestador_agent
from src.plugins import init_querybuilder_plugin

agent_orquestador = None

async def init_agent_orquestador():
    try:
        chat_service = AzureChatCompletion(
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        )

        mcp_cosmos_plugin = await McpCosmosPlugin.init_mcp_cosmos_plugin()
        query_builder_plugin = await init_querybuilder_plugin()

        agent_orquestador = ChatCompletionAgent(
            service=chat_service,
            name="AzureAssistant",
            instructions=metaprompt_orquestador_agent,
            plugins=[mcp_cosmos_plugin, query_builder_plugin, DecodificarTelegramaPlugin()],
        )
        logging.info(f"[Orquestador] agent_orquestador generado correctamente.")
        return agent_orquestador
    except Exception as e:
        logging.error(f"[Orquestador] Error: No fue posible generar agent_orquestador. {str(e)}")
        return None

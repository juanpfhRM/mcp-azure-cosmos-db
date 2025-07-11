import logging
import os

from semantic_kernel.functions import kernel_function

class QueryBuilderPlugin:
    def __init__(self, agent_querybuilder):
        self.agent_querybuilder = agent_querybuilder

    @kernel_function(
        name="consultar_cosmos_lenguaje_natural",
        description="Recibe una petición para una consulta a la base de datos. Usarse cuando se requiere construir una consulta para Azure Cosmos DB desde lenguaje natural. Retorna la consulta en SQL."
    )
    async def consultar_cosmos_func(self, peticion: str) -> str:
        try:
            completion = await self.agent_querybuilder.get_response(peticion)
            logging.info(f"[QueryBuilder] SQL generado:\n{completion.content.content}")
            return completion.content.content
        except Exception as e:
            logging.error(f"[QueryBuilder] Error: {str(e)}")
            return f"ERROR: {str(e)}"
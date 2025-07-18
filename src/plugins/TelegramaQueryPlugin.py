import logging
import os

from semantic_kernel.functions import kernel_function

class TelegramaQueryPlugin:
    def __init__(self, agent_telegramaquery):
        self.agent_telegramaquery = agent_telegramaquery

    @kernel_function(
        name="obtener_pocos_telegramas_bd",
        description="Recibe una petición para una consulta a la base de datos. Usarse cuando se requiere construir una consulta para Azure Cosmos DB desde lenguaje natural. Retorna la consulta en SQL, junto con los parámetros utilizados y el resultado obtenido."
    )
    async def obtener_pocos_telegramas_bd(self, peticion: str) -> str:
        try:
            completion = await self.agent_telegramaquery.get_response(peticion)
            logging.info(f"[TelegramaQueryPlugin] Respuesta generada:\n{completion.content.content}")
            return completion.content.content
        except Exception as e:
            logging.error(f"[TelegramaQueryPlugin] Error: {str(e)}")
            return f"ERROR: {str(e)}"
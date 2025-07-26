import logging
import os

from semantic_kernel.functions import kernel_function

class TelegramaKQueryPlugin:
    def __init__(self, agent_telegramakquery):
        self.agent_telegramakquery = agent_telegramakquery

    @kernel_function(
        name="obtener_pocos_telegramas_la",
        description="Recibe una petición para una consulta aLog Analytics. Usarse cuando se requiere construir una consulta para Azure Log Analytics desde lenguaje natural. Retorna la consulta en KQL, junto con el resultado obtenido."
    )
    async def obtener_pocos_telegramas_la(self, peticion: str) -> str:
        try:
            completion = await self.agent_telegramakquery.get_response(peticion)
            logging.info(f"[TelegramaKQueryPlugin] Respuesta generada:\n{completion.content.content}")
            return completion.content.content
        except Exception as e:
            logging.error(f"[TelegramaKQueryPlugin] Error: {str(e)}")
            return f"ERROR: {str(e)}"
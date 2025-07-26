import logging
import os

from semantic_kernel.functions import kernel_function

class TelegramaCQueryPlugin:
    def __init__(self, agent_telegramacquery):
        self.agent_telegramacquery = agent_telegramacquery

    @kernel_function(
        name="obtener_pocos_telegramas_bd",
        description="Recibe una petición para una consulta a la base de datos. Usarse cuando se requiere construir una consulta para Azure Cosmos DB desde lenguaje natural. Retorna la consulta en SQL, junto con los parámetros utilizados y el resultado obtenido."
    )
    async def obtener_pocos_telegramas_bd(self, peticion: str) -> str:
        try:
            completion = await self.agent_telegramacquery.get_response(peticion)
            logging.info(f"[TelegramaCQueryPlugin] Respuesta generada:\n{completion.content.content}")
            return completion.content.content
        except Exception as e:
            logging.error(f"[TelegramaCQueryPlugin] Error: {str(e)}")
            return f"ERROR: {str(e)}"
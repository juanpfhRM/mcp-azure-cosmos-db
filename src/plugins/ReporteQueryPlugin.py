import logging
import os

from semantic_kernel.functions import kernel_function

class ReporteQueryPlugin:
    def __init__(self, agent_reportequery):
        self.agent_reportequery = agent_reportequery

    @kernel_function(
        name="consultar_bd_reporte",
        description="Recibe una petición para una consulta a la base de datos. Usarse cuando se requiere construir una consulta para Azure Cosmos DB desde lenguaje natural. Retorna la consulta en SQL, junto con los parámetros utilizados y el resultado obtenido."
    )
    async def consultar_bd_reporte(self, peticion: str) -> str:
        try:
            completion = await self.agent_reportequery.get_response(peticion)
            logging.info(f"[ReporteQueryPlugin] Respuesta generada:\n{completion.content.content}")
            return completion.content.content
        except Exception as e:
            logging.error(f"[ReporteQueryPlugin] Error: {str(e)}")
            return f"ERROR: {str(e)}"
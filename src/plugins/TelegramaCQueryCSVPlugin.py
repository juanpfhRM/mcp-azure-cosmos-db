import json
import logging
import os
import re
import subprocess

from typing import Dict, Union

from semantic_kernel.functions import kernel_function

from src.models.CosmosSqlQuery import CosmosSqlQuery

class TelegramaCQueryCSVPlugin:
    def __init__(self, agent_telegramacquery_csv):
        self.agent_telegramacquery_csv = agent_telegramacquery_csv

    @kernel_function(
        name="obtener_varios_telegramas_bd",
        description="Recibe una petición para una consulta a la base de datos. Usarse cuando se requiere construir una consulta para Azure Cosmos DB desde lenguaje natural. Retorna la consulta en SQL, junto con los parámetros utilizados y el resultado obtenido."
    )
    async def obtener_varios_telegramas_bd(self, peticion: str) -> str:
        try:
            completion = await self.agent_telegramacquery_csv.get_response(peticion)
            logging.info(f"[TelegramaCQueryCSVPlugin] Respuesta generada:\n{completion.content.content}")
            return completion.content.content
        except Exception as e:
            logging.error(f"[TelegramaCQueryCSVPlugin] Error: {str(e)}")
            return f"ERROR: {str(e)}"

    @kernel_function(
        name="generar_csv_ctelegramas",
        description="Recibe una consulta en SQL junto con sus parámetros. Usarse cuando se requiere obtener un .CSV con todos los telegramas requeridos y su información, respectivamente. Devuelve la ruta del archivo."
    )
    def generar_csv_ctelegramas(self, sql_query_obj: CosmosSqlQuery) -> str:
        logging.info(f"[generar_csv_ctelegramas] Objeto de consulta SQL recibido: {sql_query_obj.model_dump_json()}")
        try:
            query = sql_query_obj.query
            raw_parameters_list = sql_query_obj.parameters

            logging.info(f"[generar_csv_ctelegramas] Consulta extraída: {query}")
            logging.info(f"[generar_csv_ctelegramas] Parámetros crudos (lista): {raw_parameters_list}")

            processed_parameters: Dict[str, Union[str, int, float, bool]] = {}
            if raw_parameters_list:
                for param_item in raw_parameters_list:
                    if "name" in param_item and "value" in param_item:
                        processed_parameters[param_item["name"]] = param_item["value"]
                    else:
                        logging.warning(f"[{self.__class__.__name__}.generar_csv_ctelegramas] Elemento de parámetro con formato inesperado, saltando: {param_item}")
                        raise ValueError("Algún parámetro no poseé el atributo name y/o value.")

            logging.info(f"[generar_csv_ctelegramas] Parámetros procesados (diccionario): {processed_parameters}")

            instrucciones_prohibidas = ["DELETE", "UPDATE", "INSERT INTO", "DROP", "ALTER", "TRUNCATE"]
            if any(instr in query.upper() for instr in instrucciones_prohibidas):
                raise ValueError("La consulta contiene una instrucción prohibida que modifica la base de datos.")

            final_payload = {
                "query": query,
                "parameters": processed_parameters
            }

            logging.info(f"[generar_csv_ctelegramas] Payload final para el script JS: {json.dumps(final_payload)}")

            logging.info(f"[generar_csv_ctelegramas] Ejecutando script de Node.js: src/plugins/js/generar_csv_ctelegramas.js")
            result = subprocess.run(
                ['node', 'src/plugins/js/generar_csv_ctelegramas.js'],
                input=json.dumps(final_payload),
                capture_output=True,
                text=True,
                encoding='utf-8',
                check=True
            )

            output = result.stdout.strip()
            logging.info(f"[generar_csv_ctelegramas] Salida cruda del script JS: '{output}'")

            if result.stderr:
                logging.error(f"[generar_csv_ctelegramas] Errores en stderr del script JS: '{result.stderr.strip()}'")
                raise ValueError(f"Errores en stderr del script JS: '{result.stderr.strip()}")

            if not output:
                logging.warning(f"[generar_csv_ctelegramas] El script JS no devolvió ninguna salida.")
                raise ValueError("El script JS no devolvió ninguna salida.")

            json_output = json.loads(output)
            logging.info(f"[generar_csv_ctelegramas] Salida JSON parseada del script JS: {json_output}")
            if "csv_path" not in json_output or not json_output["csv_path"]:
                logging.warning(f"[generar_csv_ctelegramas] La salida JSON del script JS no contiene 'csv_path' o está vacío.")

            return json_output

        except subprocess.CalledProcessError as e:
            return f"ERROR al ejecutar el script JS: {str(e)}"
        except json.JSONDecodeError as e:
            return f"ERROR de JSON: {str(e)}"
        except Exception as e:
            return f"ERROR: {str(e)}"
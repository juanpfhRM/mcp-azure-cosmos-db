import json
import logging
import subprocess

from semantic_kernel.functions import kernel_function

from src.models.LogAnalyticsKqlQuery import LogAnalyticsKqlQuery

class TelegramaKQueryCSVPlugin:
    def __init__(self, agent_telegramakquery_csv):
        self.agent_telegramakquery_csv = agent_telegramakquery_csv

    @kernel_function(
        name="obtener_varios_telegramas_bdla",
        description="Recibe una petición para una consulta a la base de datos. Usarse cuando se requiere construir una consulta para Azure Log Analytics desde lenguaje natural. Retorna la consulta en KQL."
    )
    async def obtener_varios_telegramas_la(self, peticion: str) -> str:
        try:
            completion = await self.agent_telegramakquery_csv.get_response(peticion)
            logging.info(f"[TelegramaKQueryCSVPlugin] Respuesta generada:\n{completion.content.content}")
            return completion.content.content
        except Exception as e:
            logging.error(f"[TelegramaKQueryCSVPlugin] Error: {str(e)}")
            return f"ERROR: {str(e)}"

    @kernel_function(
        name="generar_csv_ktelegramas",
        description="Recibe una consulta en KQL. Usarse cuando se requiere obtener un .CSV con todos los telegramas requeridos y su información, respectivamente. Devuelve la ruta del archivo."
    )
    def generar_csv_ktelegramas(self, kql_query: LogAnalyticsKqlQuery) -> str:
        logging.info(f"[generar_csv_ktelegramas] KQL recibido: {kql_query}")
        try:
            query = kql_query.query

            final_payload = {
                "query": query
            }

            print(json.dumps(final_payload))

            logging.info(f"[generar_csv_ktelegramas] Ejecutando script de Node.js: src/plugins/js/generar_csv_ktelegramas.js")
            result = subprocess.run(
                ['node', 'src/plugins/js/generar_csv_ktelegramas.js'],
                input=json.dumps(final_payload),
                capture_output=True,
                text=True,
                encoding='utf-8',
                check=True
            )

            output = result.stdout.strip()
            logging.info(f"[generar_csv_ktelegramas] Salida cruda del script JS: '{output}'")

            if result.stderr:
                logging.error(f"[generar_csv_ktelegramas] Errores en stderr del script JS: '{result.stderr.strip()}'")
                print("aaa")
                raise ValueError(f"Errores en stderr del script JS: '{result.stderr.strip()}")

            if not output:
                logging.warning(f"[generar_csv_ktelegramas] El script JS no devolvió ninguna salida.")
                print("eee")
                raise ValueError("El script JS no devolvió ninguna salida.")

            json_output = json.loads(output)
            logging.info(f"[generar_csv_ktelegramas] Salida JSON parseada del script JS: {json_output}")
            if "csv_path" not in json_output or not json_output["csv_path"]:
                print("iii")
                logging.warning(f"[generar_csv_ktelegramas] La salida JSON del script JS no contiene 'csv_path' o está vacío.")

            return json_output

        except subprocess.CalledProcessError as e:
            return f"ERROR al ejecutar el script JS: {str(e)}"
        except json.JSONDecodeError as e:
            return f"ERROR de JSON: {str(e)}"
        except Exception as e:
            return f"ERROR: {str(e)}"

# plugin = TelegramaCQueryCSVPlugin(agent_telegramakquery_csv=None)
# print(plugin.generar_csv_ktelegramas(kql_query="""ContainerLogV2 | where Type == 'ContainerLogV2' | where PodNamespace == 'cambrica' | where PodName contains "-socket-service-cambrica-" | where LogMessage contains "Telegrama procesado" | parse LogMessage with * "Tiempo total: " totalMs: int " ms. Desde PLC -> Integration Services " integrationService: string " ms, Llamada a SAP " sap: string " ms, Llamada a Persistencia " persistencia: int " ms, Desde Persistencia a envio queue de respuesta " queueRespuesta: string " ms, Desde queue de respuesta a respuesta PLC " respuestaPlc: string " ms, Telegrama original: \\"" telegrama_original: string "\\", TelegramaRespuesta: \\"" telegrama_respuesta: string "\\", SAP Data:"  sap_data: string | extend messageType = extract(@'"MessageType":"([^"]+)"', 1, sap_data) | project LocalTime=format_datetime(datetime_add('hour', -6, TimeGenerated), 'yyyy-MM-dd HH:mm:ss'), totalMs, integrationService, sap, respuestaPlc, messageType, LogMessage | take 1"""))

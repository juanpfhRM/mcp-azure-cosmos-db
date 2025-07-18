# src\plugins\FechaPlugin.py
import logging
from datetime import datetime, timedelta
from semantic_kernel.functions import kernel_function

class FechaPlugin:
    @staticmethod
    @kernel_function(name="obtener_fecha_actual" , description="Obtine la fecha actual del sistema, usarse cuando alguna instrucción SQL requiera alguna fecha como parámetro.")
    def obtener_fecha_actual() -> str:
        """
        Método que retorna la fecha actual del sistema.
        """
        try:
            ahora = datetime.now()
            logging.info(f"[FechaPlugin] Se accedió a la herramienta.")
            return ahora.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            return f"ERROR: {str(e)}"

    @staticmethod
    @kernel_function(
        name="obtener_fecha_ayer",
        description="Devuelve la fecha de ayer (formato YYYY-MM-DD)."
    )
    def obtener_fecha_ayer() -> str:
        try:
            ayer = datetime.now() - timedelta(days=1)
            return ayer.strftime("%Y-%m-%d")
        except Exception as e:
            return f"ERROR: {str(e)}"

    @staticmethod
    @kernel_function(
        name="obtener_lunes_esta_semana",
        description="Devuelve la fecha del lunes de esta semana (formato YYYY-MM-DD)."
    )
    def obtener_lunes_esta_semana() -> str:
        try:
            hoy = datetime.now()
            lunes = hoy - timedelta(days=hoy.weekday())
            return lunes.strftime("%Y-%m-%d")
        except Exception as e:
            return f"ERROR: {str(e)}"

    @staticmethod
    @kernel_function(
        name="obtener_lunes_semana_pasada",
        description="Devuelve la fecha del lunes de la semana pasada (formato YYYY-MM-DD)."
    )
    def obtener_lunes_semana_pasada() -> str:
        try:
            hoy = datetime.now()
            lunes_pasado = hoy - timedelta(days=hoy.weekday() + 7)
            return lunes_pasado.strftime("%Y-%m-%d")
        except Exception as e:
            return f"ERROR: {str(e)}"

    @staticmethod
    @kernel_function(
        name="obtener_primer_dia_mes",
        description="Devuelve la fecha del primer día del mes actual (formato YYYY-MM-DD)."
    )
    def obtener_primer_dia_mes() -> str:
        try:
            hoy = datetime.now()
            primero = datetime(hoy.year, hoy.month, 1)
            return primero.strftime("%Y-%m-%d")
        except Exception as e:
            return f"ERROR: {str(e)}"
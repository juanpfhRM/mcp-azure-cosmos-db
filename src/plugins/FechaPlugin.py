from datetime import datetime
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
            return ahora.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            return f"ERROR: {str(e)}"
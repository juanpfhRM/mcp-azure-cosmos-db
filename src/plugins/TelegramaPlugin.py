import base64
from semantic_kernel.functions import kernel_function

class TelegramaPlugin:
    @staticmethod
    @kernel_function(name="convertir_telegrama_base_64" , description="Recibe una cadena. Usarse cuando el usuario busca por valor de telegrama. Verifica que vengan los caracteres de control (02 y 03), si no los agrega, convierte a base64 y usa este valor para consultar en la base de datos.")
    def generar_base64_telegrama(telegrama: str) -> str:
        """
        Recibe un telegrama en texto, asegura que tenga caracteres de control \x02 y \x03,
        lo convierte a base64 y lo retorna.
        """
        try:
            if not telegrama.startswith('\x02'):
                telegrama = '\x02' + telegrama
            if not telegrama.endswith('\x03'):
                telegrama = telegrama + '\x03'

            telegrama_bytes = telegrama.encode("ascii")
            telegrama_base64 = base64.b64encode(telegrama_bytes).decode("ascii")
            return telegrama_base64
        except Exception as e:
            return f"ERROR: {str(e)}"
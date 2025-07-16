import logging
import base64
from semantic_kernel.functions import kernel_function

class CodificarTelegramaPlugin:
    @staticmethod
    @kernel_function(name="codificar_base64_telegrama" , description="Recibe una cadena. Convierte un telegrama de texto plano a base64 agregando caracteres de control (STX \x02 y ETX \x03) si faltan. Úsalo cuando el usuario busca por valor de telegrama.")
    def codificar_base64_telegrama(telegrama: str) -> str:
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
            logging.info(f"[TelegramaPlugin] Se accedió a la herramienta.")
            return telegrama_base64
        except Exception as e:
            return f"ERROR: {str(e)}"

    @staticmethod
    @kernel_function(
        name="decodificar_base64_telegrama",
        description="Recibe una cadena en base64, la decodifica y remueve caracteres de control STX (\\x02) y ETX (\\x03). Úsalo cuando se necesita ver el telegrama original en texto."
    )
    def decodificar_base64_telegrama(telegrama_base64: str) -> str:
        """
        Recibe una cadena en base64, la decodifica a texto ASCII,
        remueve caracteres de control \x02 (STX) y \x03 (ETX) si están presentes,
        y retorna el telegrama en texto plano.
        """
        try:
            telegrama_bytes = base64.b64decode(telegrama_base64)
            telegrama_texto = telegrama_bytes.decode("ascii")

            if telegrama_texto.startswith('\x02'):
                telegrama_texto = telegrama_texto[1:]
            if telegrama_texto.endswith('\x03'):
                telegrama_texto = telegrama_texto[:-1]

            logging.info(f"[TelegramaPlugin] Se decodificó el telegrama.")
            return telegrama_texto
        except Exception as e:
            return f"ERROR: {str(e)}"
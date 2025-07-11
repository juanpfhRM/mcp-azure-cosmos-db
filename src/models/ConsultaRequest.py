from pydantic import BaseModel

class ConsultaRequest(BaseModel):
    mensaje: str
    user_id: str
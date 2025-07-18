from pydantic import BaseModel

class ChatResponse(BaseModel):
    response: str
    csv_path: str
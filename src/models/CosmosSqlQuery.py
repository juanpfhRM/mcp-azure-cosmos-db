from typing import Optional, Dict, Union
from pydantic import BaseModel, ConfigDict

class CosmosSqlQuery(BaseModel):
    """
    Representa una consulta SQL para Azure Cosmos DB junto con sus parámetros.
    """
    query: str
    parameters: Optional[Dict[str, Union[str, int, float, bool]]] = None

    model_config = ConfigDict(extra="forbid")
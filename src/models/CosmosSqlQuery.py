from typing import Optional, Dict, Union, List
from pydantic import BaseModel, ConfigDict

class CosmosSqlQueryResult(BaseModel):
    """
    Representa una consulta SQL para Azure Cosmos DB junto con sus parámetros y resultado.
    """
    query: str
    # parameters: Optional[Dict[str, Union[str, int, float, bool]]] = None
    parameters: Optional[List[Dict[str, Union[str, int, float, bool]]]] = None
    result: str

    model_config = ConfigDict(extra="forbid")

class CosmosSqlQuery(BaseModel):
    """
    Representa una consulta SQL para Azure Cosmos DB junto con sus parámetros y resultado.
    """
    query: str
    # parameters: Optional[Dict[str, Union[str, int, float, bool]]] = None
    parameters: Optional[List[Dict[str, Union[str, int, float, bool]]]] = None

    model_config = ConfigDict(extra="forbid")
from typing import Optional, Dict, Union, List
from pydantic import BaseModel, ConfigDict

class LogAnalyticsKqlQueryResult(BaseModel):
    """
    Representa una consulta KQL para Azure Log Analytics junto con su resultado.
    """
    query: str
    result: str

    model_config = ConfigDict(extra="forbid")

class LogAnalyticsKqlQuery(BaseModel):
    """
    Representa una consulta KQL para Azure Log Analytics.
    """
    query: str
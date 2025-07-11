import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from semantic_kernel.agents import ChatHistoryAgentThread

from src.agents import Orquestador
from src.models.ConsultaRequest import ConsultaRequest
from src.plugins.mcp import McpCosmosPlugin
from src.utils.Threads import obtener_thread

router = APIRouter()
logging.basicConfig(level=logging.INFO)

@router.post("")
async def chat(req: ConsultaRequest):
    if not McpCosmosPlugin.mcp_cosmos_plugin:
        return JSONResponse(
            status_code=500,
            content={"error1"}
        )
    if not Orquestador.agent_orquestador:
        return JSONResponse(
            status_code=500,
            content={"error2"}
        )

    try:
        thread = obtener_thread(req.user_id)
        response = await Orquestador.agent_orquestador.get_response(
            messages=req.mensaje,
            thread=thread,
        )
        return {"respuesta": str(response)}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
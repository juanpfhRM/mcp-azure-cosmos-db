import logging
import json

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from semantic_kernel.agents import ChatHistoryAgentThread

from src.agents import Orquestador
from src.models.ConsultaRequest import ConsultaRequest
from src.utils.Threads import obtener_thread

router = APIRouter()
logging.basicConfig(level=logging.INFO)

@router.post("")
async def chat(req: ConsultaRequest):
    try:
        thread = obtener_thread(req.user_id)
        logging.info(f"[Chat] Prompt: {str(req.mensaje)}")
        completion = await Orquestador.agent_orquestador.get_response(
            messages=req.mensaje,
            thread=thread,
        )
        logging.info(f"[Chat] Completion: {str(completion)}")
        return json.loads(str(completion))
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
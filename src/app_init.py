from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.agents import Orquestador
from src.plugins.mcp.cosmos import McpCosmosPlugin
from src.plugins.mcp.logAnalytics import McpLogAnalyticsPlugin
from src.routes import IndexRoutes, ChatRoutes

@asynccontextmanager
async def lifespan(app: FastAPI):
    agent_orquestador = await Orquestador.init_agent_orquestador()
    Orquestador.agent_orquestador = agent_orquestador

    yield

    if McpLogAnalyticsPlugin.mcp_log_analytics_plugin:
        await McpLogAnalyticsPlugin.mcp_log_analytics_plugin.__aexit__(None, None, None)
    if McpCosmosPlugin.mcp_cosmos_plugin:
        await McpCosmosPlugin.mcp_cosmos_plugin.__aexit__(None, None, None)

def init_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    app.mount("/docs/telegramas", StaticFiles(directory="docs/telegramas"), name="telegramas")

    app.include_router(IndexRoutes.router, prefix="")
    app.include_router(ChatRoutes.router, prefix="/chat")

    return app

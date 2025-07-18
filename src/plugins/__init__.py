from src.agents.ReporteQuery import init_agent_reportquery
from src.agents.TelegramaQuery import init_agent_telegramaquery
from src.agents.TelegramaQueryCSV import init_agent_telegramaquery_csv
from src.plugins.ReporteQueryPlugin import ReporteQueryPlugin
from src.plugins.TelegramaQueryPlugin import TelegramaQueryPlugin
from src.plugins.TelegramaQueryCSVPlugin import TelegramaQueryCSVPlugin

async def init_reportequery_plugin():
    agent = await init_agent_reportquery()
    return ReporteQueryPlugin(agent)

async def init_telegramaquery_plugin():
    agent = await init_agent_telegramaquery()
    return TelegramaQueryPlugin(agent)

async def init_telegramaquery_csv_plugin():
    agent = await init_agent_telegramaquery_csv()
    return TelegramaQueryCSVPlugin(agent)
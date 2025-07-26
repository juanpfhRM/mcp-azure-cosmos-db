from src.agents.ReporteCQuery import init_agent_reportecquery
from src.agents.TelegramaCQuery import init_agent_telegramacquery
from src.agents.TelegramaKQuery import init_agent_telegramakquery
from src.agents.TelegramaCQueryCSV import init_agent_telegramacquery_csv
from src.agents.TelegramaKQueryCSV import init_agent_telegramakquery_csv
from src.plugins.ReporteCQueryPlugin import ReporteCQueryPlugin
from src.plugins.TelegramaCQueryPlugin import TelegramaCQueryPlugin
from src.plugins.TelegramaKQueryPlugin import TelegramaKQueryPlugin
from src.plugins.TelegramaCQueryCSVPlugin import TelegramaCQueryCSVPlugin
from src.plugins.TelegramaKQueryCSVPlugin import TelegramaKQueryCSVPlugin

async def init_reportecquery_plugin():
    agent = await init_agent_reportecquery()
    return ReporteCQueryPlugin(agent)

async def init_telegramacquery_plugin():
    agent = await init_agent_telegramacquery()
    return TelegramaCQueryPlugin(agent)

async def init_telegramakquery_plugin():
    agent = await init_agent_telegramakquery()
    return TelegramaKQueryPlugin(agent)

async def init_telegramacquery_csv_plugin():
    agent = await init_agent_telegramacquery_csv()
    return TelegramaCQueryCSVPlugin(agent)

async def init_telegramakquery_csv_plugin():
    agent = await init_agent_telegramakquery_csv()
    return TelegramaKQueryCSVPlugin(agent)
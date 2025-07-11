from src.agents.QueryBuilder import init_agent_querybuilder
from src.plugins.QueryBuilderPlugin import QueryBuilderPlugin

async def init_querybuilder_plugin():
    agent = await init_agent_querybuilder()
    return QueryBuilderPlugin(agent)

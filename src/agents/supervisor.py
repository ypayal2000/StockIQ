# from src.utils.logger import logger
# from src.agents.symbol_extractor import SymbolExtractor
# from src.agents.router_llm import RouterLLM

# extractor = SymbolExtractor()
# router = RouterLLM()

# class SupervisorAgent:

#     def route(self, state):

#         query = state["user_query"]
#         state["symbol"] = extractor.extract(query)

#         route = router.route(query)
#         state["route"] = route

#         logger.info(f"Detected Symbol: {state['symbol']}")
#         logger.info(f"Selected Route: {route}")

#         return state

from src.agents.symbol_extractor import SymbolExtractor
from src.agents.planner_agent import PlannerAgent

from src.utils.logger import logger


extractor = SymbolExtractor()
planner = PlannerAgent()


class SupervisorAgent:

    def route(self, state):

        query = state["user_query"]
        symbol = extractor.extract(query)
        agents = planner.plan(query)

        state["symbol"] = symbol
        state["agents"] = agents

        logger.info(f"Detected Symbol: {symbol}")
        logger.info( f"Selected Agents: {agents}")

        return state
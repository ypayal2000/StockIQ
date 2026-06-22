from langgraph.graph import StateGraph, END

from src.agents.state import StockState

from src.agents.supervisor import SupervisorAgent
from src.agents.executor_agent import ExecutorAgent
from src.agents.aggregator_agent import AggregatorAgent


supervisor = SupervisorAgent()
executor = ExecutorAgent()
aggregator = AggregatorAgent()


def supervisor_node(state):
    return supervisor.route(state)


def executor_node(state):
    return executor.run(state)


def aggregator_node(state):

    agents = state.get("agents", [])

    # Investment workflow

    if len(agents) > 1:
        return aggregator.run(state)

    # News only

    if "news" in agents:
        state["response"] = state["news_result"]
        return state

    # Prediction only

    if "prediction" in agents:
        state["response"] = state["prediction_result"]
        return state

    # Analysis only

    if "analysis" in agents:
        state["response"] = state["analysis_result"]
        return state

    return state


graph = StateGraph(StockState)

graph.add_node("supervisor", supervisor_node)
graph.add_node("executor", executor_node)
graph.add_node("aggregator", aggregator_node)

graph.set_entry_point("supervisor")

graph.add_edge("supervisor", "executor")
graph.add_edge("executor", "aggregator")
graph.add_edge("aggregator", END)

graph = graph.compile()
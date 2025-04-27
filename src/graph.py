from src.nodes import (
    query_analysis_node,
    search_and_scrape,
    split_into_searches,
    summarizer_node,
)
from src.state import InputState, OutputState, State
from src.configuration import Configuration
from langgraph.graph import StateGraph, END

workflow = StateGraph(
    State, input=InputState, output=OutputState, config_schema=Configuration
)
workflow.add_node("query_analysis_node", query_analysis_node)
workflow.add_node("search_and_scrape", search_and_scrape)
workflow.add_node("summarizer_node", summarizer_node)
workflow.add_edge("__start__", "query_analysis_node")
workflow.add_conditional_edges(
    "query_analysis_node", split_into_searches, ["search_and_scrape"]
)
workflow.add_edge("search_and_scrape", "summarizer_node")
workflow.add_edge("summarizer_node", END)


graph = workflow.compile()
graph.name = "ResearcherGraph"

from langgraph.graph import StateGraph, START, END

from state import NewsState
from nodes.extractor import extractor_node
from nodes.summarizer import summarizer_node
from nodes.keypoints import keypoints_node
from nodes.conclusion import conclusion_node
from nodes.formatter import formatter_node


def build_graph():
    graph = StateGraph(NewsState)

    graph.add_node("extractor",  extractor_node)
    graph.add_node("summarizer", summarizer_node)
    graph.add_node("keypoints",  keypoints_node)
    graph.add_node("conclusion", conclusion_node)
    graph.add_node("formatter",  formatter_node)

    graph.add_edge(START,        "extractor")
    graph.add_edge("extractor",  "summarizer")
    graph.add_edge("summarizer", "keypoints")
    graph.add_edge("keypoints",  "conclusion")
    graph.add_edge("conclusion", "formatter")
    graph.add_edge("formatter",  END)

    return graph.compile()

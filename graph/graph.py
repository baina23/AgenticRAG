from dotenv import load_dotenv
from langgraph.graph import END, StateGraph

from graph.consts import RETRIEVE, GRADE_DOCUMENTS, GENERATION, WEB_SEARCH
from graph.nodes import generate, grade_documents, web_search, retrieve
from graph.state import GraphState

load_dotenv()

def decide_to_generate(state):
    print("---ASSESS GRADED DOCUMENTS---")

    if state["web_search"]:
        print(
            "---DECISION: NOT ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION---"
        )
        return WEB_SEARCH
    else:
        print("---DECISION: GENERATE---")
        return GENERATION

workflow = StateGraph(GraphState)

workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(WEB_SEARCH, web_search)
workflow.add_node(GENERATION, generate)

workflow.set_entry_point(RETRIEVE)
workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)
workflow.add_conditional_edges(
    GRADE_DOCUMENTS,
    decide_to_generate,
    {
        WEB_SEARCH: WEB_SEARCH,
        GENERATION: GENERATION,
    },
)
workflow.add_edge(WEB_SEARCH, GENERATION)
workflow.add_edge(GENERATION, END)

app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="graph.png")







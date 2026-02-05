from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from typing import TypedDict
from functools import partial


class RecipeState(TypedDict):
    dish: str
    ingredients: str
    recipe: str


def generate_recipe_node(state: RecipeState, llm):
    """Node to generate recipe using LLM."""
    prompt = f"Generate a recipe for {state['dish']} with ingredients: {state['ingredients']}."
    response = llm.invoke(prompt)
    return {"recipe": response.content}


def create_recipe_graph(llm):
    """Create and compile the recipe generation graph."""
    graph = StateGraph(RecipeState)
    node_func = partial(generate_recipe_node, llm=llm)
    graph.add_node("generate_recipe", node_func)
    graph.add_edge(START, "generate_recipe")
    graph.add_edge("generate_recipe", END)
    return graph.compile()

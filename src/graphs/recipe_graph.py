from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from typing import TypedDict
from functools import partial
from src.utils.config_models import RecipeState


def create_node_func(prompt_template, llm):
    """Helper to create node function with prompt."""

    def node_func(state):
        prompt = prompt_template.format(**state)
        response = llm.invoke(prompt)
        return {
            key: response.content
            for key in state.keys()
            if key
            in [
                "ingredientes",
                "titulo_receita",
                "descricao_receita",
                "modo_preparo",
                "tags",
                "ingredientes_convertidos",
                "imagem_path",
                "receita_final_md",
            ]
        }

    return node_func


def extract_ingredients_node(state, llm, prompt_template):
    prompt = prompt_template.format(receita_texto=state["receita_texto"])
    response = llm.invoke(prompt)
    return {"ingredientes": response.content}


def extract_title_node(state, llm, prompt_template):
    prompt = prompt_template.format(receita_texto=state["receita_texto"])
    response = llm.invoke(prompt)
    return {"titulo_receita": response.content}


def extract_description_node(state, llm, prompt_template):
    prompt = prompt_template.format(receita_texto=state["receita_texto"])
    response = llm.invoke(prompt)
    return {"descricao_receita": response.content}


def extract_preparation_node(state, llm, prompt_template):
    prompt = prompt_template.format(receita_texto=state["receita_texto"])
    response = llm.invoke(prompt)
    return {"modo_preparo": response.content}


def generate_tags_node(state, llm, prompt_template):
    prompt = prompt_template.format(receita_texto=state["receita_texto"])
    response = llm.invoke(prompt)
    return {"tags": response.content}


def convert_measurements_node(state, llm, prompt_template):
    prompt = prompt_template.format(lista_ingredientes=state["ingredientes"])
    response = llm.invoke(prompt)
    return {"ingredientes_convertidos": response.content}


def generate_image_node(state, llm, prompt_template):
    prompt = prompt_template.format(
        titulo_receita=state["titulo_receita"],
        descricao_receita=state["descricao_receita"],
    )
    response = llm.invoke(prompt)
    # Placeholder for image generation
    return {"imagem_path": f"Imagem gerada: {response.content}"}


def compile_recipe_node(state, llm, prompt_template):
    prompt = prompt_template.format(
        titulo=state["titulo_receita"],
        descricao=state["descricao_receita"],
        ingredientes_convertidos=state["ingredientes_convertidos"],
        modo_preparo=state["modo_preparo"],
        tags=state["tags"],
    )
    response = llm.invoke(prompt)
    return {"receita_final_md": response.content}


def create_recipe_graph(llm, cfg):
    """Create and compile the recipe processing graph."""
    graph = StateGraph(RecipeState)

    # Add nodes with partial functions
    graph.add_node(
        "extract_ingredients",
        partial(
            extract_ingredients_node,
            llm=llm,
            prompt_template=cfg.system.ingredient_extractor,
        ),
    )
    graph.add_node(
        "extract_title",
        partial(
            extract_title_node, llm=llm, prompt_template=cfg.system.title_extractor
        ),
    )
    graph.add_node(
        "extract_description",
        partial(
            extract_description_node,
            llm=llm,
            prompt_template=cfg.system.description_extractor,
        ),
    )
    graph.add_node(
        "extract_preparation",
        partial(
            extract_preparation_node,
            llm=llm,
            prompt_template=cfg.system.preparation_extractor,
        ),
    )
    graph.add_node(
        "generate_tags",
        partial(generate_tags_node, llm=llm, prompt_template=cfg.system.tag_generator),
    )
    graph.add_node(
        "convert_measurements",
        partial(
            convert_measurements_node,
            llm=llm,
            prompt_template=cfg.system.measurement_converter,
        ),
    )
    graph.add_node(
        "generate_image",
        partial(
            generate_image_node, llm=llm, prompt_template=cfg.system.image_generator
        ),
    )
    graph.add_node(
        "compile_recipe",
        partial(
            compile_recipe_node, llm=llm, prompt_template=cfg.system.recipe_compiler
        ),
    )

    # Add edges based on context
    graph.add_edge(START, "extract_ingredients")
    graph.add_edge(START, "extract_title")
    graph.add_edge(START, "extract_description")
    graph.add_edge(START, "extract_preparation")
    graph.add_edge(START, "generate_tags")
    graph.add_edge("extract_ingredients", "convert_measurements")
    graph.add_edge("extract_title", "generate_image")
    graph.add_edge("extract_description", "generate_image")
    graph.add_edge("extract_title", "compile_recipe")
    graph.add_edge("extract_description", "compile_recipe")
    graph.add_edge("convert_measurements", "compile_recipe")
    graph.add_edge("extract_preparation", "compile_recipe")
    graph.add_edge("generate_tags", "compile_recipe")
    graph.add_edge("generate_image", END)
    graph.add_edge("compile_recipe", END)

    return graph.compile()

import hydra
from omegaconf import DictConfig
from langchain_ollama import ChatOllama
from src.utils.config_models import LLMConfig, AppConfig
from src.graphs.recipe_graph import create_recipe_graph


@hydra.main(config_path="../configs", config_name="app_config", version_base=None)
def main(cfg: DictConfig):
    # Validate configs with Pydantic
    llm_config = LLMConfig(**cfg.models)
    app_config = AppConfig(**cfg.app)

    # Create LLM instance
    llm = ChatOllama(
        model=llm_config.model,
        base_url=llm_config.base_url,
        temperature=llm_config.temperature,
    )

    # Create and run the graph
    graph = create_recipe_graph(llm)
    result = graph.invoke(
        {"dish": "pasta", "ingredients": "tomato, basil, garlic", "recipe": ""}
    )

    print("Generated Recipe:")
    print(result["recipe"])


if __name__ == "__main__":
    main()

import hydra
from omegaconf import DictConfig
from langchain_ollama import ChatOllama
from src.utils.config_models import LLMConfig, AppConfig
from src.graphs.recipe_graph import create_recipe_graph


@hydra.main(config_path="../configs", config_name="app_config", version_base=None)
def main(cfg: DictConfig):
    # Validate configs with Pydantic
    print(cfg.app)
    llm_config = LLMConfig(**cfg.models.ollama)
    app_config = AppConfig(**cfg.app)

    # Create LLM instance
    llm = ChatOllama(
        model=llm_config.model,
        base_url=llm_config.base_url,
        temperature=llm_config.temperature,
    )

    # Create and run the graph
    graph = create_recipe_graph(llm, cfg.agents)
    result = graph.invoke(
        {
            "receita_texto": app_config.receita_texto,
            "ingredientes": "",
            "titulo_receita": "",
            "descricao_receita": "",
            "modo_preparo": "",
            "tags": "",
            "ingredientes_convertidos": "",
            "imagem_path": "",
            "receita_final_md": "",
        }
    )

    print("Processed Recipe:")
    print(result["receita_final_md"])


if __name__ == "__main__":
    main()

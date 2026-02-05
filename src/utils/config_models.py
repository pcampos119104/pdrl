from pydantic import BaseModel
from typing import TypedDict


class LLMConfig(BaseModel):
    model: str
    base_url: str
    temperature: float
    max_tokens: int


class PromptConfig(BaseModel):
    system: dict[str, str]
    user: dict[str, str]


class AppConfig(BaseModel):
    debug: bool
    timeout: int
    paths: dict[str, str]
    receita_texto: str


class RecipeState(TypedDict):
    receita_texto: str
    ingredientes: str
    titulo_receita: str
    descricao_receita: str
    modo_preparo: str
    tags: str
    ingredientes_convertidos: str
    imagem_path: str
    receita_final_md: str

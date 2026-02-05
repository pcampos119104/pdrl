from pydantic import BaseModel


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

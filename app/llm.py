from langchain_openai import ChatOpenAI

from app.core.config import settings


def get_llm(temperature: float = 0) -> ChatOpenAI:
    return ChatOpenAI(
        base_url=settings.azure_ai_endpoint,
        api_key=settings.azure_ai_api_key,
        model=settings.azure_ai_model,
        temperature=temperature,
    )

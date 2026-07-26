import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    azure_ai_endpoint: str = os.environ["AZURE_AI_ENDPOINT"]
    azure_ai_api_key: str = os.environ["AZURE_AI_API_KEY"]
    azure_ai_model: str = os.environ["AZURE_AI_MODEL"]


settings = Settings()

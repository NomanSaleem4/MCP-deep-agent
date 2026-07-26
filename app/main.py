import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logger import setup_logging
from app.calculator.tools import tools
from app.llm import get_llm
from app.calculator import routes
from app.agent_factory import factory

setup_logging(logging.INFO)
log = logging.getLogger(__name__)

SYSTEM_PROMPT = (Path(__file__).parent / "agents.md").read_text()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.agent = factory.build_agent(
        llm=get_llm(), tools=tools, system_prompt=SYSTEM_PROMPT
    )
    yield
    app.state.agent = None


app = FastAPI(lifespan=lifespan)
app.include_router(routes.query_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

import logging
from pathlib import Path
from typing import Any, List, Optional

from deepagents import create_deep_agent
from deepagents.backends import LocalShellBackend

log = logging.getLogger(__name__)

PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)


class AgentFactory:
    """Factory responsible for initializing and configuring Deep Agent instances."""

    def __init__(
        self,
        root_dir: str = PROJECT_ROOT,
        memory_paths: Optional[List[str]] = None,
    ):
        self.root_dir = root_dir
        self.memory_paths = memory_paths or ["./app/calculator/memory/facts.md"]

    def _get_backend(self) -> LocalShellBackend:
        return LocalShellBackend(
            root_dir=self.root_dir,
            inherit_env=True,
            virtual_mode=True,
        )

    def build_agent(self, llm: Any, tools: List[Any], system_prompt: str):
        log.info("Loaded tools: %s", [getattr(t, "name", str(t)) for t in tools])

        return create_deep_agent(
            model=llm,
            tools=tools,
            system_prompt=system_prompt,
            memory=self.memory_paths,
            backend=self._get_backend(),
        )


factory = AgentFactory()

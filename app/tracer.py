import json
import os
import time
from langchain_core.callbacks import BaseCallbackHandler


class FileTracer(BaseCallbackHandler):
    def __init__(self, trace_file="logs/traces.jsonl"):
        os.makedirs(os.path.dirname(trace_file), exist_ok=True)
        self.trace_file = trace_file

    def _write(self, event: str, data: dict):
        record = {"time": time.strftime("%Y-%m-%dT%H:%M:%S"), "event": event, **data}
        with open(self.trace_file, "a") as f:
            f.write(json.dumps(record) + "\n")

    def on_llm_start(self, serialized, prompts, **kwargs):
        self._write("llm_start", {"prompts": prompts})

    def on_llm_end(self, response, **kwargs):
        generation = response.generations[0][0] if response.generations else None
        text = generation.text if generation else ""
        tool_calls = []
        if generation and hasattr(generation, "message"):
            tool_calls = [
                {"tool": tc["name"], "args": tc["args"]}
                for tc in generation.message.additional_kwargs.get("tool_calls", [])
            ] or [
                {"tool": tc.get("name"), "args": tc.get("args")}
                for tc in getattr(generation.message, "tool_calls", [])
            ]
        self._write("llm_end", {"response": text, "tool_calls": tool_calls})

    def on_tool_start(self, serialized, input_str, **kwargs):
        self._write("tool_start", {"tool": serialized.get("name"), "input": input_str})

    def on_tool_end(self, output, **kwargs):
        self._write("tool_end", {"output": str(output)})

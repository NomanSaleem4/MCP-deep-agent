from app.tracer import FileTracer


async def stream(agent, query: str):
    async for event in agent.astream_events(
        {"messages": [{"role": "user", "content": query}]},
        version="v2",
        config={"callbacks": [FileTracer()]},
    ):
        if event["event"] == "on_chat_model_stream":
            chunk = event["data"]["chunk"]
            if chunk.content:
                yield f"data: {chunk.content}\n\n"
    yield "data: [DONE]\n\n"

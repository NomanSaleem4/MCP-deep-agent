import logging

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from app.calculator.schemas import QueryRequest
from app.calculator.services import stream

log = logging.getLogger(__name__)

query_router = APIRouter(prefix="/api/agent", tags=["Agent"])


@query_router.post("/query")
async def query_agent(req: QueryRequest, request: Request):
    log.info("Received query: %s", req.query)
    return StreamingResponse(
        stream(request.app.state.agent, req.query), media_type="text/event-stream"
    )

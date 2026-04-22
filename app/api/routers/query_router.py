from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse

from app.api.dependencies import get_query_services
from app.api.schemas.query_schema import QuerySchema
from app.services.query_services import QueryService

query_router = APIRouter()

@query_router.post("/api/query")
async def query_handler(query: QuerySchema, query_service: Annotated[QueryService, Depends(get_query_services)]):
    return StreamingResponse(query_service.query(query.query), media_type="text/event-stream")

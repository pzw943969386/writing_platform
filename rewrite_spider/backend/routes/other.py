from fastapi import APIRouter
from pydantic import BaseModel


other_router = APIRouter()


class SplitTextRequest(BaseModel):
    text: str


@other_router.post("/split_text")
async def split_text(request: SplitTextRequest):
    text = request.text
    lines = [s for s in text.split("。") if s]
    result = "。\n\n".join(lines)
    return {"text": result}
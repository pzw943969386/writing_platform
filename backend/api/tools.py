from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import re
from ..models.tools_model import SplitTextResponse

tools_router = APIRouter()


class SplitTextRequest(BaseModel):
    text: str


@tools_router.post("/split_text")
async def split_text(request: SplitTextRequest):
    text = request.text
    try:
        lines = re.split(r"。(?![：:＊*])", text)

        # 过滤空字符串并重新添加句号
        result_lines = []
        for i, line in enumerate(lines):
            if line.strip():
                if i < len(lines) - 1:
                    result_lines.append(line + "。")
                else:
                    result_lines.append(line)

        result = "\n\n".join(result_lines)
        return SplitTextResponse(message="success", code=200, data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分割文本失败: {e}")

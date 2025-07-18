from fastapi import APIRouter
from pydantic import BaseModel
import re

other_router = APIRouter()


class SplitTextRequest(BaseModel):
    text: str


@other_router.post("/split_text")
async def split_text(request: SplitTextRequest):
    text = request.text
    
    # 使用正则表达式进行分割
    # 匹配句号，但后面不能是冒号或星号
    # (?![：:＊*]) 是负向前瞻，确保句号后面不是冒号或星号
    lines = re.split(r'。(?![：:＊*])', text)
    
    # 过滤空字符串并重新添加句号
    result_lines = []
    for i, line in enumerate(lines):
        if line.strip():  # 确保不是空字符串
            if i < len(lines) - 1:  # 不是最后一行
                result_lines.append(line + "。")
            else:  # 最后一行
                result_lines.append(line)
    
    result = "\n\n".join(result_lines)
    return {"text": result}
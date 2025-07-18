from pydantic import BaseModel, ConfigDict


class SplitTextResponse(BaseModel):
    message: str
    code: int
    data: str

    model_config = ConfigDict(
        json_schema_extra={"example": {"message": "success", "code": 200, "data": ""}}
    )

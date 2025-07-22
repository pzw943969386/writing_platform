from openai import AsyncOpenAI
from loguru import logger


class LLMProvider:
    def __init__(self, config: dict):
        self.api_key = config.get("api_key")
        self.base_url = config.get("base_url")
        self.model = config.get("model")
        self.client = AsyncOpenAI(api_key=self.api_key)

    async def response(self, messages: list[dict]):
        try:
            response = await self.client.chat.completions.create(
                model=self.model, messages=messages, stream=True
            )
            async for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            logger.error(f"LLMProvider response error: {e}")

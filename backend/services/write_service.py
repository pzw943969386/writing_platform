from ..core.providers.llm.openai import LLMProvider
from ..config.setting import settings


class WriteService:
    def __init__(self):
        self.glm_provider = LLMProvider(config=settings.glm)
        self.kimi_provider = LLMProvider(config=settings.kimi)

    def read_prompt_from_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: File {file_path} not found.")
            return None
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None

    async def analyze_article(self, article_text, analysis_prompt):
        messages = [
            {"role": "system", "content": "你是人工智能助手"},
            {"role": "user", "content": analysis_prompt},
            {
                "role": "assistant",
                "content": '我已准备好以"文章分析专家"的身份为你服务。请把需要深度解析的文章完整粘贴（或上传可复制的文本），我将按照"内容-结构-手法-语言-受众"五大维度，逐层拆解其写作精髓，并给出可立即上手的学习建议。',
            },
            {"role": "user", "content": article_text},
        ]

        try:
            # 使用非流式获取完整响应
            response = await self.glm_provider.get_response(messages)
            if response and response.choices:
                return response.choices[0].message.content
            else:
                return "分析失败：未获得有效响应"
        except Exception as e:
            print(f"分析文章时出错: {e}")
            return f"分析失败：{str(e)}"

    async def rewrite_article_stream(
        self,
        analysis_data: str,
        rewrite_prompt: str,
    ):
        """重写文章，返回流式响应"""

        messages = [
            {"role": "system", "content": "你是人工智能助手"},
            {"role": "user", "content": rewrite_prompt},
            {
                "role": "assistant",
                "content": "好的，我已准备好接收您提供的分析框架和内容。请将需要重构的要点、结构或原始材料发给我，我将依据上述原则为您撰写一篇流畅、有深度、易读的文章。",
            },
            {"role": "user", "content": analysis_data},
        ]

        try:
            async for chunk in self.glm_provider.stream_response(messages):
                yield chunk
        except Exception as e:
            print(f"重写文章时出错: {e}")
            yield f"重写失败：{str(e)}"

    async def write_article(self, article_content: str):
        analysis_prompt = self.read_prompt_from_file("./backend/services/analysis.md")
        rewrite_prompt = self.read_prompt_from_file("./backend/services/rewrite.md")

        analysis_data = await self.analyze_article(article_content, analysis_prompt)

        async for chunk in self.rewrite_article_stream(
            analysis_data, rewrite_prompt
        ):
            yield chunk


write_service = WriteService()

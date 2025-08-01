from openai import OpenAI
import os


def read_prompt_from_file(file_path):
    """Read prompt content from a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def get_volces_client():
    """Create and return an OpenAI client configured for Volces API."""
    return OpenAI(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key="",
    )


def get_bigmodel_client():
    """Create and return an OpenAI client configured for BigModel API."""
    return OpenAI(
        base_url="https://open.bigmodel.cn/api/paas/v4",
        api_key="",
    )


def analyze_article(client, article_text, analysis_prompt, model="glm-4.5"):
    """Analyze an article using the provided client and prompt."""
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是人工智能助手"},
            {"role": "user", "content": analysis_prompt},
            {
                "role": "assistant",
                "content": '我已准备好以"文章分析专家"的身份为你服务。请把需要深度解析的文章完整粘贴（或上传可复制的文本），我将按照"内容-结构-手法-语言-受众"五大维度，逐层拆解其写作精髓，并给出可立即上手的学习建议。',
            },
            {"role": "user", "content": article_text},
        ],
    )
    return completion.choices[0].message.content


def rewrite_article(client, analysis_data, rewrite_prompt, model="glm-4.5"):
    """Rewrite an article analysis using the provided client and prompt."""
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是人工智能助手"},
            {"role": "user", "content": rewrite_prompt},
            {
                "role": "assistant",
                "content": "好的，我已准备好接收您提供的分析框架和内容。请将需要重构的要点、结构或原始材料发给我，我将依据上述原则为您撰写一篇流畅、有深度、易读的文章。",
            },
            {"role": "user", "content": analysis_data},
        ],
    )
    return completion.choices[0].message.content


def main():
    # Read prompts from files
    analysis_prompt = read_prompt_from_file("./analsis.md")
    rewrite_prompt = read_prompt_from_file("./rewrite.md")

    if not analysis_prompt or not rewrite_prompt:
        print("Failed to read prompt files. Exiting.")
        return

    article = """
鸡蛋在日常生活中算得上性价比很高的食物，不仅价格亲民，还能做成水煮蛋、荷包蛋、炸鸡蛋等多种样式。
图片
它富含优质蛋白、铁、钙、胡萝卜素等营养元素，几乎集齐了健康食品该有的所有优点。
不过 “树大招风”，这几年关于鸡蛋的负面说法不少，有人说它是心血管杀手，常吃会损害血管，这是真的吗？

每天早上吃个水煮蛋，到底是营养好选择，还是伤害血管的隐患呢？

图片
先看水煮蛋的营养价值。它属于高蛋白、低脂肪的食物，不仅有优质蛋白，还包含维生素 B₂、维生素 D、磷和铁等成分，从营养角度来说确实很丰富。

有人觉得水煮蛋会伤血管，是因为它含有胆固醇。医学顶级期刊《circulation循环》杂志上曾有中南大学襄阳二医院主导的研究，结论提到血清总胆固醇升高与心血管疾病死亡风险有关联，每升高一个梯度，死亡风险就增加 14%。

再加上很多人觉得胆固醇是动脉硬化和冠心病的元凶，于是对水煮蛋，尤其是蛋黄避之不及，觉得不能多吃。

图片
但实际上，健康人的身体能自行调节胆固醇合成：摄入多了，自身合成就会减少，同时分解增多；反之则会增加合成。人体出现血脂异常，主要是内分泌或血脂代谢失调、高血压、肥胖、活动量不足等因素导致的。所以没必要把鸡蛋想得太可怕，正常食用对健康不会有太大影响。

相反，有研究显示，每周吃 4-7 个鸡蛋能保护心脏，降低心脏病风险；每天一个水煮蛋还能帮助控制体重，减少脂肪摄入，从而降低肥胖和糖尿病的发病可能。

不过鸡蛋虽好，这 3 种却不适合常吃：

图片
一是糖心蛋。这种没彻底煮熟的鸡蛋，可能含有沙门氏菌，没煮熟就会让细菌残留，人吃了容易出现腹泻、呕吐、发烧。如果不确定鸡蛋是否足够安全，尽量别做糖心蛋。

图片
二是毛鸡蛋。很多人喜欢吃这种未孵化成型的鸡蛋，觉得营养价值高，却不知道它如果没煮熟，更容易让人感染沙门氏菌，而且毛鸡蛋比普通鸡蛋更难彻底做熟。

图片
三是炸鸡蛋。在螺蛳粉、过桥米线和不少人的早餐里，都能看到炸鸡蛋的身影。但鸡蛋经过高温油炸后，营养价值会大量流失，热量却大幅增加，长期吃会加重心血管和肝脏的负担。

另外，高温油炸还可能产生环烷氨等有害物质，增加患癌或心血管疾病的风险。

图片
除此之外，这几类人吃鸡蛋要谨慎：

肾脏病患者不宜多吃。这类患者新陈代谢较慢，体内代谢产物无法完全排出，若吃太多鸡蛋，可能加重肾脏负担、恶化病情，严重时还会引发尿毒症，威胁健康。

蛋白过敏者要注意。鸡蛋含蛋白质，对鸡蛋蛋白过敏的人吃了后，可能出现腹泻、消化不良、皮疹等反应。

正在服用磺胺类药物和碳酸氢钠的人，也建议少吃或不吃鸡蛋。服用磺胺类药物时吃太多鸡蛋，蛋白在体内代谢产生的酸性物质可能形成结石；而碳酸氢钠遇酸会分解，吃鸡蛋可能降低药效。
"""

    glm_client = get_bigmodel_client()
    glm_model = "glm-4.5"

    volces_client = get_volces_client()
    ki_model = "ep-20250729141508-nw7h2"

    analysis_data = analyze_article(volces_client, article, analysis_prompt, ki_model)

    rewrite_data = rewrite_article(glm_client, analysis_data, rewrite_prompt, glm_model)

    print(rewrite_data)


if __name__ == "__main__":
    main()

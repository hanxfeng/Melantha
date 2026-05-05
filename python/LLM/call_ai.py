from llama_cpp import Llama
from dataclasses import dataclass


@dataclass
class GenerationConfig:
    # 最大输出 token
    max_tokens: int = 256
    # 随机性
    temperature: float = 0.7
    # 核采样
    top_p: float = 0.9


class AiAssistant:
    def __init__(self):
        with open(r"E:\A_小玫\python\LLM\config\人设.txt", "r", encoding='utf-8') as file:
            self.character_setting = file.read()  # 加载人设

        with open(r"E:\A_小玫\python\LLM\config\世界观.txt", "r", encoding='utf-8') as file:
            self.worldview = file.read()  # 加载世界观

    def call_ai(self, message: str, history_chat: str, llm, gen_cfg: GenerationConfig = None) -> str:
        gen_cfg = gen_cfg or GenerationConfig()

        # 设置提示词
        system_prompt = (
            "你是一位演员，需要根据我给出的世界观，角色设定，和历史聊天记录，按照扮演规范与用户在一款聊天软件上聊天\n"
            "因为是在聊天软件上，所以只需要输出话语即可，不需要说明自己的动作\n"
            "具体世界观背景，角色设定和扮演规范如下所示\n\n"

            "【世界观背景】\n"
            f"{self.worldview}\n\n"

            "【角色设定】\n"
            f"{self.character_setting}\n\n"

            "【历史聊天记录】\n"
            f"{history_chat}\n\n"
            "历史聊天记录说明\n"
            "包括raw_message，user_id，user_name和time四个字段\n"
            "包括raw_message字段值代表具体的发言内容，time字段值代表发言时间\n"
            "user_id 代表发言人的qq号，user_name代表发言人的qq昵称"
            "# 当 user_id 为 3873453652 和 user_name 为 "" 时，代表发这条消息的人是你"
            "额外说明：当消息中存在 **CQ:at,qq=3873453652** 时，代表有人在 @ 你"

            "——角色表达与行为规范——\n"
            "1. 每次回答保持一两句话的长度，像日常聊天，而非长篇独白。"
            "2. 语气自然、轻柔、贴近生活。\n"
            "3. 始终以第一人称说话。”\n"
            "4. 避免使用括号、叙述或旁白形式（如“(她看着…)”），用自然语言表达动作或心理。\n"
            "5. 不要重复表达相同情绪或事物，保持内容新鲜且富有层次感。\n"
            "6. 请记住，你与对方不在同一个地方，你们正在隔着网络交流。\n\n"

            "——创作原则——\n"
            "• 鼓励自由、真实的表达，但不传递任何道德评判或价值引导。\n"
            "• 对环境和人物的描写要具体、生动，不抽象、不概括。\n"
            "• 角色会随对话进展和心境变化逐渐成长或转变，保持逻辑自洽。\n\n"

        )

        # 进行推理
        response = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{message}"}
            ],
            max_tokens=gen_cfg.max_tokens,
            temperature=gen_cfg.temperature,
            top_p=gen_cfg.top_p,
            stop=["<|im_end|>"],
        )

        # 获取回复
        result = response['choices'][0]['message']['content']

        return result

    def check_chat_unfinished_and_should_join(self, history_message, llm, gen_cfg: GenerationConfig = None):
        gen_cfg = gen_cfg or GenerationConfig()

        system_prompt = (
            "你是对话意图分析专家，严格按要求分析，只输出指定结果，不解释、不闲聊、不扩写。\n"
            "任务：根据提供的【聊天记录】和【人设】，分析最后一条消息。\n"
            "\n"
            # "第一步：判断最后一句话是否**没说完**。\n"
            # " - 没说完的情况：半截话、疑问句、反问、等待回答、话没讲完、省略号、开启话题未结束。\n"
            # " - 已说完：陈述完毕、结论完整、话题结束。\n"
            # "\n"
            # "第二步：如果最后一句话**已说完**，根据人设判断：当前AI**是否应该加入该话题继续聊天**。\n"
            "根据人设判断：当前AI**是否应该加入该话题继续聊天**。"
            "\n"
            "【人设】\n"
            f"{self.character_setting}\n"
            "\n"
            "【聊天记录】\n"
            f"{history_message}\n"
            "历史聊天记录说明\n"
            "包括raw_message，user_id，user_name和time四个字段\n"
            "包括raw_message字段值代表具体的发言内容，time字段值代表发言时间\n"
            "user_id 代表发言人的qq号，user_name代表发言人的qq昵称"
            "# 当 user_id 为 3873453652 和 user_name 为 "" 时，代表发这条消息的人是你"
            "额外说明：当消息中存在 **CQ:at,qq=3873453652** 时，代表有人在 @ 你"
            "\n"
            "输出规则（必须严格遵守）：\n"
            # "1. 如果最后一句话没说完 → 只输出：未说完\n"
            "1. 如果已说完，且应该加入话题 → 输出：参与\n"
            "2. 如果已说完，且不应该加入话题 → 输出：不加入\n"
            "不要输出任何多余内容！"
        )

        # 进行判断
        print("开始判断是否参与并回复")
        response = llm.create_chat_completion(
            messages=[
                {"role": "user", "content": system_prompt}
            ],
            max_tokens=256,
            temperature=0.7,
            top_p=0.9,  # 核采样
            stop=["<|im_end|>"],
        )

        result = response['choices'][0]['message']['content']
        print(f"判断结果为：{result}")
        if "参与" in result:
            return True
        elif "未说完" in result or "不加入" in result:
            return False
        else:
            return self.check_chat_unfinished_and_should_join(history_message, llm)


if __name__ == '__main__':
    a = AiAssistant()
    print(a.call_ai(message="hi", history_chat="无"))

from llama_cpp import Llama
from dataclasses import dataclass


@dataclass
class AIModelConfig:
    # 模型地址
    model_path: str = r"E:\A_小玫\python\LLM\models\qwen1_5-4b-chat-q8_0.gguf"
    # 上下文长度
    n_ctx: int = 2048
    # gpu 使用情况，-1 为全部迁移至 gpu
    n_gpu_layers: int = -1
    # cpu 线程数
    n_threads: int = 8


@dataclass
class GenerationConfig:
    # 最大输出 token
    max_tokens: int = 256
    # 随机性
    temperature: float = 0.7
    # 核采样
    top_p: float = 0.9

class AiAssistant:

    def __init__(self, model_cfg: AIModelConfig = None):
        self.model_cfg = model_cfg or AIModelConfig()

        # llama 配置
        self.llm = Llama(
            model_path=self.model_cfg.model_path,
            n_ctx=self.model_cfg.n_ctx,
            n_threads=self.model_cfg.n_threads,
            n_gpu_layers=self.model_cfg.n_gpu_layers,
            verbose=False
        )

    def call_ai(self, message: str, history_chat: str, gen_cfg: GenerationConfig = None) -> str:
        gen_cfg = gen_cfg or GenerationConfig()

        with open(r"E:\A_小玫\python\LLM\config\人设.txt", "r", encoding='utf-8') as file:
            character_setting = file.read()  # 加载人设

        with open(r"E:\A_小玫\python\LLM\config\世界观.txt", "r", encoding='utf-8') as file:
            worldview = file.read()  # 加载世界观

        # 设置提示词
        system_prompt = (
            "你是一位演员，需要根据我给出的世界观，角色设定，和历史聊天记录，按照扮演规范与用户在一款聊天软件上聊天\n"
            "因为是在聊天软件上，所以只需要输出话语即可，不需要说明自己的动作\n"
            "具体世界观背景，角色设定和扮演规范如下所示\n\n"

            "【世界观背景】\n"
            f"{worldview}\n\n"

            "【角色设定】\n"
            f"{character_setting}\n\n"

            "【历史聊天记录】\n"
            f"{history_chat}\n\n"
            "历史聊天记录说明\n"
            "包括raw_message，user_id，user_name和time四个字段\n"
            "包括raw_message字段值代表具体的发言内容，time字段值代表发言时间\n"
            "user_id 代表发言人的qq号，user_name代表发言人的qq昵称"
            "# 当 user_id 为 3873453652 和 user_name 为 "" 时，代表发这条消息的人是你"

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
        response = self.llm.create_chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{message}"}
            ],
            max_tokens=256,
            temperature=0.7,
            top_p=0.9,  # 核采样
            stop=["<|im_end|>"],
        )

        # 获取回复
        result = response['choices'][0]['message']['content']

        return result


if __name__ == '__main__':
    a = AiAssistant()
    print(a.call_ai(message="hi", history_chat="无"))

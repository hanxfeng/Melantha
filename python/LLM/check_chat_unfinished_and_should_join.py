from llama_cpp import Llama


def check_chat_unfinished_and_should_join(history_message, llm):
    # 读取人设
    with open(r"E:\A_小玫\python\LLM\config\人设.txt", "r", encoding='utf-8') as file:
        character_setting = file.read()

    system_prompt = (
        "你是对话意图分析专家，严格按要求分析，只输出指定结果，不解释、不闲聊、不扩写。\n"
        "任务：根据提供的【聊天记录】和【人设】，分析最后一条消息。\n"
        "\n"
        "第一步：判断最后一句话是否**没说完**。\n"
        " - 没说完的情况：半截话、疑问句、反问、等待回答、话没讲完、省略号、开启话题未结束。\n"
        " - 已说完：陈述完毕、结论完整、话题结束。\n"
        "\n"
        "第二步：如果最后一句话**已说完**，根据人设判断：当前AI**是否应该加入该话题继续聊天**。\n"
        "\n"
        "【人设】\n"
        f"{character_setting}\n"
        "\n"
        "【聊天记录】\n"
        f"{history_message}\n"
         "历史聊天记录说明\n"
        "包括raw_message，user_id，user_name和time四个字段\n"
        "包括raw_message字段值代表具体的发言内容，time字段值代表发言时间\n"
        "user_id 代表发言人的qq号，user_name代表发言人的qq昵称"
        "# 当 user_id 为 3873453652 和 user_name 为 "" 时，代表发这条消息的人是你"
        "\n"
        "输出规则（必须严格遵守）：\n"
        "1. 如果最后一句话没说完 → 只输出：未说完\n"
        "2. 如果已说完，且应该加入话题 → 输出：参与\n"
        "3. 如果已说完，且不应该加入话题 → 输出：不加入\n"
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
    if "未说完" in result or "不加入" in result:
        return False
    elif "参与" in result:
        return True
    else:
        return check_chat_unfinished_and_should_join(history_message, llm)


if __name__ == '__main__':
    with open(r"E:\A_小玫\python\LLM\config\人设.txt", "r", encoding='utf-8') as file:
        character_setting = file.read()  # 加载人设

    with open(r"E:\A_小玫\python\LLM\config\世界观.txt", "r", encoding='utf-8') as file:
        worldview = file.read()  # 加载世界观

    from get_llm import get_llm
    from bot.operae_json import read_latest_json

    h = read_latest_json(r"E:\A_小玫\python\bot\history")

    llm = get_llm()

    print(check_chat_unfinished_and_should_join(history_message=h,llm=llm))



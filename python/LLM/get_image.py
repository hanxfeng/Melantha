import os
import random


def get_image(history_message: str, llm):
    image_path = r"E:\A_小玫\python\LLM\images"
    # 获取图片
    image_files = [f for f in os.listdir(image_path) if f.endswith(('.jpg', '.png', 'gif'))]
    if not image_files:
        return None

    # 2. 从文件名中提取情感描述（去掉扩展名）
    emotion_labels = [os.path.splitext(f)[0] for f in image_files]

    # 构建提示词
    system_prompt = (
        "你是情感分析+表情适配判断专家。请根据给定聊天记录完成两项任务：\n"
        "1. 判断聊天中**最新一条消息**是否适合添加表情；\n"
        "2. 如果需要添加表情，从指定情感标签中，选择**最匹配**的1个情感标签；\n"
        "输出格式要求：严格按一行输出，如果不需要添加表情则输出不需要，否则输出情感标签\n"
        "---\n"
        "聊天记录：\n"
        f"{history_message}\n"
        "---\n"
        "可用的情感标签：\n"
        f"{', '.join(emotion_labels)}\n"
        "规则：仅从给定标签选一个，不自创；根据最新消息语气、语境、聊天氛围判断是否适合加表情，只允许不需要或情感标签；严格遵守格式，不要多余解释、不要换行。"
    )


    # 进行推理
    print("开始进行图片选择")
    response = llm.create_chat_completion(
        messages=[
            {"role": "user", "content": system_prompt}
        ],
        max_tokens=256,
        temperature=0.7,
        top_p=0.9,  # 核采样
        stop=["<|im_end|>"],
    )

    # 获取回复
    result = response['choices'][0]['message']['content']
    print(f"图片选择模型回复为”{result}“")
    if "不需要" in result:
        return False

    # 获取候选图片列表
    images_list = []
    for f in image_files:
        if result in f:
            images_list.append(f)

    result_image = random.choice(images_list)

    return r"E:\A_小玫\python\LLM\images\\" + str(result_image)


if __name__ == '__main__':
    print(get_image(""))

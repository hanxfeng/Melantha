import asyncio
import json
import websockets
from LLM.call_ai import AiAssistant
from operae_json import read_latest_json, save_message
from LLM.get_image import GetImage
from LLM.get_llm import get_llm


async def get_message(message_data, websocket, llm, ai_assistant, get_Image):
    # 解析消息

    print(f"message:{message_data}")

    # 确保是消息事件，并获取关键信息
    if message_data.get("post_type") == "message":
        # 处理群聊消息
        if message_data.get("message_type") == "group":

            group_id = message_data.get("group_id")
            print(f"群号为：{group_id}")
            # if group_id == 794339782:
            if group_id == 937129319:

                # 获取当前消息
                push_message = message_data.get("raw_message")

                # 获取历史消息
                history_chat = read_latest_json()

                # 判断是否要回复消息
                flag = ai_assistant.check_chat_unfinished_and_should_join(history_message=history_chat, llm=llm)

                if not flag:
                    return ""

                print(f"收到消息：”{push_message}“，开始推理")

                # 获取 ai 回复

                reply_message = ai_assistant.call_ai(message=push_message, history_chat=history_chat, llm=llm)

                # 保存 ai 回复
                save_message(reply_message, ai=True)
                reply_message = {"type": "text", "data": {"text": f"{reply_message}"}}

                # 选择图片
                image_path = get_Image.get_image(history_chat, llm)

                # 根据图片类型确定发送方式
                if image_path:
                    reply_image = {"type": "image", "data": {"file": image_path}}
                else:
                    reply_image = False

                # 分别发送回复
                await send_group_message(websocket, group_id, reply_message)

                # 如果存在图片消息则发送
                if reply_image:
                    await asyncio.sleep(0.1)
                    await send_group_message(websocket, group_id, reply_image)


async def send_group_message(websocket, group_id, message):
    # 构建标准 API 请求包
    await websocket.send(json.dumps({
        "action": "send_group_msg",
        "params": {
            "group_id": group_id,
            "message": message
        }
    }))


def save_now_message(message_data):
    # 解析消息
    message = json.loads(message_data)
    print(f"message:{message}")

    # 确保是消息事件，并获取关键信息
    if message.get("post_type") == "message":
        # 处理群聊消息
        if message.get("message_type") == "group":

            group_id = message.get("group_id")
            print(f"群号为：{group_id}")
            # if group_id == 794339782:
            if group_id == 937129319:
                # 保存聊天记录
                return save_message(message)


async def listen_to_napcat(llm):
    token = "QSGebDrUedfsdaKY"
    uri = f"ws://127.0.0.1:3001?access_token={token}"
    print("操作已开始")

    ai_assistant = AiAssistant()
    get_Image = GetImage()

    while True:
        try:
            async with websockets.connect(uri) as websocket:
                # 创建一个容量为 1 的队列，自动保留最新消息
                msg_queue = asyncio.Queue(maxsize=1)

            # 接收任务
                async def receiver():
                    async for raw_message in websocket:
                        save_now_message(raw_message)
                        msg_dict_queue = json.loads(raw_message)

                        if msg_dict_queue is None:
                            continue
                        # 如果队列已满，丢弃旧消息（即只保留最新）
                        if msg_queue.full():
                            try:
                                msg_queue.get_nowait()
                            except asyncio.QueueEmpty:
                                pass
                        await msg_queue.put(msg_dict_queue)

                # 处理任务
                async def processor():
                    while True:
                        msg_dict = await msg_queue.get()
                        await get_message(
                            message_data=msg_dict,
                            websocket=websocket,
                            llm=llm,
                            ai_assistant=ai_assistant,
                            get_Image=get_Image,
                        )

                    # 并发运行接收和处理任务

                await asyncio.gather(receiver(), processor())

        except (websockets.ConnectionClosed, OSError) as e:
            print(f"连接断开或错误: {e}，正在重连...")
            await asyncio.sleep(1)
            continue


if __name__ == "__main__":
    llm = get_llm()
    asyncio.run(listen_to_napcat(llm))

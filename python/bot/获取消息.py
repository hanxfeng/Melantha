import asyncio
import json
import websockets
import os
from datetime import datetime
from LLM.call_ai import AiAssistant
from operae_json import read_latest_json,save_message


async def get_message(message_data, websocket):
    # 解析消息
    message = json.loads(message_data)
    print(f"message:{message}")

    # 确保是消息事件，并获取关键信息
    if message.get("post_type") == "message":
        # 处理群聊消息
        if message.get("message_type") == "group":

            group_id = message.get("group_id")
            print(f"群号为：{group_id}")
            if group_id == 937129319:
                dict = save_message(message)
                push_message = dict.get("raw_message")
                history_chat = read_latest_json()

                print(f"收到消息：{push_message}，开始推理")

                ai_assistant = AiAssistant()
                reply_message = ai_assistant.call_ai(message=push_message, history_chat=history_chat)

                save_message(reply_message, ai=True)

                # 发送回复
                await send_group_message(websocket, group_id, reply_message)

        """
        # 处理群聊消息
        if message_type == "group":
            group_id = message.get("group_id")
            # 检查消息是否包含 'CQ:at,qq=' 标签，并且 @ 的是机器人自己
            if f"CQ:at,qq={self_id}" in raw_message:
                # 提取消息内容（去除 @ 标签和多余空格）
                clean_msg = raw_message.replace(f"[CQ:at,qq={self_id}]", "").strip()
                # 如果消息内容是“今日时间”
                if clean_msg == "今日时间":
                    # 生成当前时间
                    now = datetime.now()
                    current_time = now.strftime("%Y年%m月%d日 %H:%M:%S")
                    reply_message = f"现在时间是：{current_time}"

                    # 异步发送回复
                    await send_group_message(websocket, group_id, reply_message)
                    print(f"已回复群 {group_id} 中 {user_id} 的消息")
                    """


async def send_group_message(websocket, group_id, message):
    # 构建标准 API 请求包
    await websocket.send(json.dumps({
        "action": "send_group_msg",
        "params": {
            "group_id": group_id,
            "message": message
        }
    }))


async def listen_to_napcat():
    token = "QSGebDrUedfsdaKY"
    uri = f"ws://127.0.0.1:3001?access_token={token}"
    print("操作已开始")
    # 持续监听 WebSocket 消息
    async for websocket in websockets.connect(uri):
        try:
            async for message in websocket:
                await get_message(message, websocket)
        except websockets.ConnectionClosed:
            print("连接已断开，正在尝试重新连接...")
            continue


if __name__ == "__main__":
    asyncio.run(listen_to_napcat())

import os
import json
from datetime import datetime


def save_message(message, base_dir="./history", ai=False):
    """
    用于将传入的消息保存至本地
    :param ai: 值为 True 时保存 ai 回复，值为 False 时，保存发送者回复
    :param message: 传入的消息
    :param base_dir: 文件的保存文件夹
    :return: 转变为字典格式的数据
    """

    now = datetime.now()
    folder_name = now.strftime("%Y-%m-%d")
    file_name = now.strftime("%H")
    file_path = os.path.join(base_dir, folder_name, f"{file_name}.json")

    # 创建文件夹（如果不存在）
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    if ai :
        # 当 user_id 为 3873453652 和 user_name 为 "" 时，代表发这条消息的人是你
        dict_message = {
            "raw_message": message,
            "user_id": 3873453652,
            "user_name": "",
            "time": str(now)
        }

        # 将数据转换为 JSON 字符串（确保中文不转义）
        json_line = json.dumps(dict_message, ensure_ascii=False) + '\n'

        # 追加写入文件
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(json_line)

        return dict_message

    else:
        # 获取时间并构建文件夹名和文件名


        # 将数据转为字典格式
        # 消息内容
        raw_message = message.get("raw_message", "")
        # 发消息的人的 qq 号
        user_id = message.get("user_id")
        # 发消息的人的昵称
        user_name = message.get("sender").get("nickname")
        # bot 的 qq 号
        self_id = message.get("self_id")

        # 创建字典格式数据
        dict_message = {
            "raw_message": raw_message,
            "user_id": user_id,
            "user_name": user_name,
            "time": str(now)
        }

        # 将数据转换为 JSON 字符串（确保中文不转义）
        json_line = json.dumps(dict_message, ensure_ascii=False) + '\n'

        # 追加写入文件
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(json_line)

        return dict_message


def read_latest_json(base_dir='./history'):
    """
    读取最新保存的 JSON 文件。
    根据之前 save_json_data 的规则：文件夹名为 YYYY-MM-DD，文件名为 HH-MM-SS.json，
    每行存储一个 JSON 对象。
    返回:
        如果找到文件：
            - return_last_only=False 时，返回 list，包含文件中的所有 Python 对象。
            - return_last_only=True 时，返回单个 Python 对象（最后一条）。
        如果未找到任何符合条件的文件，返回 None。
    """
    # 存储所有符合日期格式的文件夹及其日期对象
    date_folders = []

    try:
        for item in os.listdir(base_dir):
            full_path = os.path.join(base_dir, item)
            if os.path.isdir(full_path):
                # 检查文件夹名是否符合 YYYY-MM-DD 格式
                try:
                    folder_date = datetime.strptime(item, "%Y-%m-%d")
                    date_folders.append((folder_date, full_path))
                except ValueError:
                    continue  # 不是日期文件夹，跳过
    except FileNotFoundError:
        return None

    if not date_folders:
        return None

    # 按日期排序，取得最新的文件夹
    latest_date, latest_folder = max(date_folders, key=lambda x: x[0])

    # 在最新文件夹中找到符合 HH-MM-SS.json 格式的文件
    json_files = []
    for filename in os.listdir(latest_folder):
        if filename.endswith('.json'):
            # 尝试解析文件名时间部分
            name_part = filename[:-5]  # 去掉 .json
            try:
                # 检查是否符合 HH-MM-SS 格式（例如 14-30-45）
                time_obj = datetime.strptime(name_part, "%H")
                json_files.append((name_part, filename, time_obj))
            except ValueError:
                continue

    if not json_files:
        return None

    # 按时间排序，取最新的文件
    latest_file = max(json_files, key=lambda x: x[2])[1]
    file_path = os.path.join(latest_folder, latest_file)

    # 读取文件内容
    data_list = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:  # 跳过空行
                try:
                    data_list.append(json.loads(line))
                except json.JSONDecodeError:
                    # 如果某行不是合法 JSON，可以选择忽略或抛出异常
                    # 这里简单忽略并继续
                    continue

    if not data_list:
        return "无"

    return data_list


# 示例使用
if __name__ == '__main__':
    # 假设已经用之前的 save_json_data 保存了一些数据

    # 读取所有已保存的记录（列表形式）
    all_data = read_latest_json(base_dir='./history')
    if all_data:
        print(f"最新文件中的所有数据（共 {len(all_data)} 条）:")
        print(all_data)

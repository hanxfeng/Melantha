from llama_cpp import Llama

# ========== 配置区域 ==========
# 根据你下载的模型文件，修改为实际路径
# 推荐：DeepSeek-R1-Distill-Qwen-1.5B-Q4_K_M.gguf 或 7B-Q3_K_S.gguf
model_path = r"E:\A_小玫\python\LLM\models\Llama-3.2-1B-Instruct-Q6_K.gguf"

# 上下文长度：1.5B 可用 4096，7B 建议从 2048 开始测试
n_ctx = 2048*40

# GPU 加速：-1 表示全部层加载到 GPU（显存足够时）
n_gpu_layers = -1

# CPU 线程数（根据你的 CPU 核心数调整）
n_threads = 8
# =============================

llm = Llama(
    model_path=model_path,
    n_ctx=int(n_ctx),
    n_threads=n_threads,
    n_gpu_layers=n_gpu_layers,
    verbose=False,
    # 可选：设置随机种子保证可复现
    # seed=1337,
)

# 使用聊天补全接口（自动处理 DeepSeek-R1-Distill-Qwen 需要的模板）
system_prompt = ""
response = llm.create_chat_completion(
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "你好？"}
    ],
    max_tokens=256,          # 最大生成长度
    temperature=0.7,         # 随机性
    top_p=0.9,               # 核采样
    stop=["<|im_end|>"],     # 遇到对话结束符时停止
)

# 提取并打印模型回复
reply = response['choices'][0]['message']['content']
print(reply)
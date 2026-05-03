from llama_cpp import Llama


def get_llm():
    llm = Llama(
        model_path=r"E:\A_小玫\python\LLM\models\qwen1_5-4b-chat-q8_0.gguf",
        n_ctx=2048,
        n_threads=8,
        n_gpu_layers=-1,
        verbose=False
    )
    return llm
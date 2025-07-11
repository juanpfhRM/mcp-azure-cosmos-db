from semantic_kernel.agents import ChatHistoryAgentThread

user_threads: dict[str, ChatHistoryAgentThread] = {}

def obtener_thread(user_id: str) -> ChatHistoryAgentThread:
    global user_threads
    if user_id not in user_threads:
        user_threads[user_id] = ChatHistoryAgentThread()
    return user_threads[user_id]
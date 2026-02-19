from langchain_ollama import ChatOllama


def get_llm():
    return ChatOllama(
        model="gemma3:latest",
        temperature=0
    )

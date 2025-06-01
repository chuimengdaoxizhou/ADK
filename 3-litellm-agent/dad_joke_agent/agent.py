import os
import random

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

OLLAMA_MODEL = "gemma3:1b"

# 使用 LiteLLM 的 Ollama 模型适配器
model = LiteLlm(
    model=f"ollama/{OLLAMA_MODEL}",
    api_base="http://localhost:11434",  # Ollama 默认端口
)


def get_dad_joke():
    jokes = [
        "Why did the chicken cross the road? To get to the other side!",
        "What do you call a belt made of watches? A waist of time.",
        "What do you call fake spaghetti? An impasta!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
    ]
    return random.choice(jokes)


root_agent = Agent(
    name="dad_joke_agent",
    model=model,
    description="Dad joke agent",
    instruction="""
    You are a helpful assistant that can tell dad jokes. 
    Only use the tool `get_dad_joke` to tell jokes.
    """,
    tools=[get_dad_joke],
)
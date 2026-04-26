import os
from pathlib import Path

from langchain_openai import ChatOpenAI

from state import NewsState

llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    model="deepseek-chat",
)

_prompt_template = Path("prompts/summarizer.txt").read_text(encoding="utf-8")


def summarizer_node(state: NewsState) -> dict:
    prompt = _prompt_template.format(cuerpo=state["cuerpo"])
    response = llm.invoke(prompt)
    return {"resumen": response.content.strip()}

import os
from pathlib import Path

from langchain_openai import ChatOpenAI

from state import NewsState

llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    model="deepseek-chat",
)

_prompt_template = Path("prompts/keypoints.txt").read_text(encoding="utf-8")


def keypoints_node(state: NewsState) -> dict:
    prompt = _prompt_template.format(cuerpo=state["cuerpo"], resumen=state["resumen"])
    response = llm.invoke(prompt)
    points = [
        line.lstrip("-•* ").strip()
        for line in response.content.strip().split("\n")
        if line.strip()
    ]
    return {"keypoints": points[:5]}

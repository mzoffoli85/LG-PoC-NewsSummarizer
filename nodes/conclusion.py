import os
from pathlib import Path

from langchain_openai import ChatOpenAI

from state import NewsState

llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    model="deepseek-chat",
)

_prompt_template = Path("prompts/conclusion.txt").read_text(encoding="utf-8")


def conclusion_node(state: NewsState) -> dict:
    prompt = _prompt_template.format(
        titular=state["titular"],
        resumen=state["resumen"],
        keypoints="\n".join(f"- {k}" for k in state["keypoints"]),
    )
    response = llm.invoke(prompt)
    return {"conclusion": response.content.strip()}

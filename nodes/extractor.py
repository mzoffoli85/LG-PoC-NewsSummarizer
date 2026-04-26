import os

import requests
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI

from state import NewsState

llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    model="deepseek-chat",
)

_PROMPT = """Extrae del siguiente texto periodístico:
- titular (título principal de la noticia)
- autor (nombre del autor, "Desconocido" si no aparece)
- fecha (fecha de publicación en formato YYYY-MM-DD, "Desconocida" si no aparece)
- cuerpo (texto principal sin anuncios ni menús)

Responde EXACTAMENTE en este formato:
TITULAR: ...
AUTOR: ...
FECHA: ...
CUERPO: ...

Texto:
{text}"""


def extractor_node(state: NewsState) -> dict:
    raw = state["input"]

    if raw.startswith("http"):
        response = requests.get(raw, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator="\n", strip=True)
    else:
        text = raw

    response = llm.invoke(_PROMPT.format(text=text[:4000]))

    data: dict = {"titular": "", "autor": "", "fecha": "", "cuerpo": ""}
    cuerpo_lines: list[str] = []
    in_cuerpo = False

    for line in response.content.strip().split("\n"):
        if line.startswith("TITULAR:"):
            data["titular"] = line.removeprefix("TITULAR:").strip()
        elif line.startswith("AUTOR:"):
            data["autor"] = line.removeprefix("AUTOR:").strip()
        elif line.startswith("FECHA:"):
            data["fecha"] = line.removeprefix("FECHA:").strip()
        elif line.startswith("CUERPO:"):
            in_cuerpo = True
            first = line.removeprefix("CUERPO:").strip()
            if first:
                cuerpo_lines.append(first)
        elif in_cuerpo:
            cuerpo_lines.append(line)

    data["cuerpo"] = "\n".join(cuerpo_lines).strip()
    return data

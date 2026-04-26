from typing import TypedDict


class NewsState(TypedDict):
    input:      str        # URL o texto raw
    titular:    str        # Node 1
    autor:      str        # Node 1
    fecha:      str        # Node 1
    cuerpo:     str        # Node 1
    resumen:    str        # Node 2
    keypoints:  list[str]  # Node 3
    conclusion: str        # Node 4
    output_md:  str        # Node 5

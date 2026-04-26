from state import NewsState


def formatter_node(state: NewsState) -> dict:
    keypoints_md = "\n".join(f"- {k}" for k in state["keypoints"])
    output_md = f"""# {state['titular']}
**Autor:** {state['autor']} | **Fecha:** {state['fecha']}

## Resumen
{state['resumen']}

## Puntos Clave
{keypoints_md}

## Conclusión
{state['conclusion']}
"""
    return {"output_md": output_md}

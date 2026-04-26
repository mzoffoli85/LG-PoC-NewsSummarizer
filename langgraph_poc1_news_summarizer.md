# LangGraph PoC #1 — News Structured Summarizer
> Este archivo es el inicializador del proyecto. Léelo completo antes de escribir una sola línea de código.

---

## Contexto del proyecto

Primer PoC de una serie de 5 construidos con **LangGraph** en Python. El foco es entender la base de LangGraph: **Graphs, Nodes y Edges** — cómo se define un flujo explícito donde cada nodo tiene una responsabilidad única.

**Serie completa:**
1. 👉 **News Summarizer** *(Graphs + Nodes + Edges)* ← este proyecto
2. ⬜ State Management
3. ⬜ Conditional Edges
4. ⬜ Human in the Loop
5. ⬜ Multi-agent con LangGraph

---

## Objetivo del PoC

Dado una URL o texto de una noticia, un grafo de nodos la procesa en etapas y genera un resumen estructurado en MD. El foco está en **definir el grafo explícitamente** — nada es implícito como en ADK.

---

## ¿Qué hace el sistema?

```
INPUT: URL o texto plano de una noticia

GRAFO:
Node 1 — Extractor   → extrae titular, autor, fecha y cuerpo
Node 2 — Summarizer  → genera resumen de 3 oraciones
Node 3 — KeyPoints   → extrae 3-5 puntos clave
Node 4 — Conclusion  → genera conclusión editorial
Node 5 — Formatter   → ensambla todo en MD estructurado

Edges: Extractor → Summarizer → KeyPoints → Conclusion → Formatter

OUTPUT: news_YYYY-MM-DD.md
```

---

## Arquitectura del grafo

```python
# Definición explícita del grafo
graph = StateGraph(NewsState)

graph.add_node("extractor",   extractor_node)
graph.add_node("summarizer",  summarizer_node)
graph.add_node("keypoints",   keypoints_node)
graph.add_node("conclusion",  conclusion_node)
graph.add_node("formatter",   formatter_node)

graph.add_edge(START,         "extractor")
graph.add_edge("extractor",   "summarizer")
graph.add_edge("summarizer",  "keypoints")
graph.add_edge("keypoints",   "conclusion")
graph.add_edge("conclusion",  "formatter")
graph.add_edge("formatter",   END)
```

---

## Estado compartido entre nodos

```python
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
```

---

## Estructura de carpetas

```
langgraph-poc1-news-summarizer/
├── main.py              # Entry point — recibe URL o texto como argumento
├── graph.py             # Definición del grafo y edges
├── state.py             # NewsState TypedDict
├── nodes/
│   ├── __init__.py
│   ├── extractor.py     # Node 1 — extrae metadata y cuerpo
│   ├── summarizer.py    # Node 2 — resume en 3 oraciones
│   ├── keypoints.py     # Node 3 — extrae puntos clave
│   ├── conclusion.py    # Node 4 — genera conclusión editorial
│   └── formatter.py     # Node 5 — ensambla MD final
├── prompts/
│   ├── summarizer.txt
│   ├── keypoints.txt
│   └── conclusion.txt
├── outputs/             # MDs generados
├── .env.example
├── requirements.txt
└── README.md
```

---

## Cómo se ejecuta

```bash
# Instalar dependencias
pip install langgraph langchain-openai python-dotenv requests beautifulsoup4

# Configurar variables de entorno
cp .env.example .env

# Ejecutar con URL
python main.py --input "https://url-de-la-noticia.com"

# Ejecutar con texto plano
python main.py --input "texto de la noticia aquí..."

# Output en: outputs/news_YYYY-MM-DD.md
```

---

## Variables de entorno

```env
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

> Este PoC usa **DeepSeek vía API directa** como LLM.
> Configurar LangChain apuntando al endpoint de DeepSeek:
> ```python
> from langchain_openai import ChatOpenAI
> llm = ChatOpenAI(
>     api_key=os.getenv("DEEPSEEK_API_KEY"),
>     base_url=os.getenv("DEEPSEEK_BASE_URL"),
>     model="deepseek-chat"
> )
> ```

---

## Formato del output esperado

```markdown
# [Titular]
**Autor:** [autor] | **Fecha:** [fecha]

## Resumen
[3 oraciones que resumen la noticia]

## Puntos Clave
- [punto 1]
- [punto 2]
- [punto 3]

## Conclusión
[Párrafo editorial con perspectiva]
```

---

## Conceptos LangGraph que se practican

| Concepto | Dónde aparece |
|---|---|
| **StateGraph** | Grafo tipado con estado compartido |
| **Nodes** | 5 nodos, cada uno con 1 responsabilidad |
| **Edges** | Conexiones explícitas entre nodos |
| **TypedDict State** | Estado que fluye y se enriquece nodo a nodo |
| **START / END** | Entry y exit point explícitos del grafo |
| **Compilación** | `graph.compile()` antes de ejecutar |

---

## Diferencia clave vs ADK

| | ADK | LangGraph |
|---|---|---|
| Flujo | Implícito, el agente decide | Explícito, vos lo defines |
| Control | El framework orquesta | Vos orquestás |
| Debug | Difícil de trazar | Cada nodo es trazable |

---

## Restricciones de scope

- ❌ No usar Conditional Edges (eso es PoC #3)
- ❌ No persistir estado entre ejecuciones (eso es PoC #2)
- ❌ No Human in the Loop (eso es PoC #4)
- ✅ Flujo lineal puro: un nodo → siguiente nodo
- ✅ Foco en que el estado se enriquezca correctamente en cada nodo

---

## Definition of Done

- [ ] `NewsState` definido con todos los campos
- [ ] 5 nodos implementados cada uno en su archivo
- [ ] Grafo compilado y ejecutable
- [ ] Edges conectan los nodos en orden correcto
- [ ] Output se guarda como `.md` en `/outputs`
- [ ] Funciona con `python main.py --input "URL o texto"`

---

## Orden de avance

```
👉 1 — Graphs + Nodes + Edges    (News Summarizer)   ← estás aquí
⬜ 2 — State Management
⬜ 3 — Conditional Edges
⬜ 4 — Human in the Loop
⬜ 5 — Multi-agent con LangGraph
```

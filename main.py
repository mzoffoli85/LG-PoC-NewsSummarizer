import argparse
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from graph import build_graph  # noqa: E402 — load_dotenv must run first


def main():
    parser = argparse.ArgumentParser(description="News Structured Summarizer")
    parser.add_argument("--input", required=True, help="URL o texto de la noticia")
    args = parser.parse_args()

    app = build_graph()
    result = app.invoke({"input": args.input})

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"news_{date.today()}.md"
    output_path.write_text(result["output_md"], encoding="utf-8")
    print(f"Output guardado en: {output_path}")


if __name__ == "__main__":
    main()

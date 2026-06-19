from pathlib import Path
from datetime import datetime
from liteparse import LiteParse


INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")


def make_output_filename(pdf_path: Path) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    clean_name = pdf_path.stem.lower().replace(" ", "-")
    return f"{clean_name}_{timestamp}.md"


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    pdf_files = list(INPUT_DIR.glob("*.pdf"))

    if not pdf_files:
        print("Geen PDF-bestanden gevonden in de input-map.")
        return

    parser = LiteParse(output_format="markdown")

    for pdf_file in pdf_files:
        print(f"Bezig met verwerken: {pdf_file.name}")

        result = parser.parse(str(pdf_file))

        output_filename = make_output_filename(pdf_file)
        output_path = OUTPUT_DIR / output_filename

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(result.text)

        print(f"Opgeslagen als: {output_path}")


if __name__ == "__main__":
    main()
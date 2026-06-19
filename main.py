from liteparse import LiteParse

pdf_file = "input/document.pdf"

parser = LiteParse(output_format="markdown")

result = parser.parse(pdf_file)

print(result.text)

with open("output.md", "w", encoding="utf-8") as file:
    file.write(result.text)

print("Markdown opgeslagen als output.md")
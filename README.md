# PDF naar Markdown Converter

Een supersnelle en gebruiksvriendelijke webapplicatie die PDF-bestanden omzet naar schone Markdown-bestanden met behulp van **LiteParse** en **Streamlit**.

LiteParse maakt gebruik van native Rust-bindings, waardoor PDF-documenten in-memory en razendsnel worden geparseerd naar gestructureerde Markdown, inclusief ocr-ondersteuning voor gescande PDF's.

---

## 🛠️ Projectstructuur

Het project is als volgt opgebouwd:

- **[main.py](main.py)**: De Streamlit webapplicatie code.
- **[pyproject.toml](pyproject.toml)**: Project-instellingen en Python-afhankelijkheden (beheerd met `uv`).
- **[input/](input/)**: (Optionele) map voor PDF-bestanden die je handmatig wilt klaarzetten of uploaden (wordt leeggehouden in Git).
- **[output/](output/)**: De map waar de geconverteerde `.md` (Markdown) bestanden lokaal worden opgeslagen.
- **[processed/](processed/)**: Map waar een kopie van de originele, verwerkte PDF-bestanden als backup wordt bewaard.

---

## 🚀 Snel Aan de Slag

Dit project maakt gebruik van **uv**, een extreem snelle Python package manager. Volg de onderstaande stappen om de applicatie te installeren en te starten.

### 1. Vereisten installeren
Zorg ervoor dat je `uv` hebt geïnstalleerd. Als je dit nog niet hebt gedaan, kun je dit als volgt installeren:

- **Windows (PowerShell):**
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- **macOS / Linux:**
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

### 2. Afhankelijkheden installeren
Navigeer naar de projectmap en installeer de benodigde packages in een virtuele omgeving:

```powershell
uv sync
```

### 3. De Streamlit App Starten
Start de applicatie met het volgende commando:

```powershell
uv run streamlit run main.py
```

De app opent automatisch in je browser (meestal op `http://localhost:8501`).

---

## 💡 Functionaliteiten

- **Snelheid & Nauwkeurigheid:** Native Rust document parser.
- **Multi-file Upload:** Sleep meerdere PDF's tegelijkertijd in de app.
- **Live Preview:** Bekijk de gegenereerde Markdown direct in de interface.
- **Batch Downloads:** Download alle succesvol geconverteerde bestanden in één ZIP-archief of download ze individueel.
- **Lokale Backup:** Slaat verwerkte bestanden en resultaten op in [processed/](processed/) en [output/](output/).
- **Fouttolerantie:** Zorgt ervoor dat één gecorrumpeerde PDF het converteren van de rest van je bestanden niet blokkeert.
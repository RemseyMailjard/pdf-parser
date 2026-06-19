from pathlib import Path
from datetime import datetime
import io
import zipfile
import streamlit as st
from liteparse import LiteParse


# Directory setup
OUTPUT_DIR = Path("output")
PROCESSED_DIR = Path("processed")

OUTPUT_DIR.mkdir(exist_ok=True)
PROCESSED_DIR.mkdir(exist_ok=True)


def make_output_filename(pdf_name: str) -> str:
    pdf_path = Path(pdf_name)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    clean_name = pdf_path.stem.lower().replace(" ", "-")
    return f"{clean_name}_{timestamp}.md"


# Initialize Session State
if "processed_results" not in st.session_state:
    st.session_state["processed_results"] = []


# Page configurations
st.set_page_config(
    page_title="PDF naar Markdown Converter",
    page_icon="📄",
    layout="wide"  # Wide layout is better for previews
)

st.title("📄 PDF naar Markdown Converter")
st.write("Upload één of meerdere PDF-bestanden om ze automatisch om te zetten naar schone Markdown met LiteParse.")

# Sidebar with local storage info and history clearing
with st.sidebar:
    st.header("Over de Converter")
    st.write(
        "Deze app gebruikt **LiteParse** met native Rust bindings om PDF-documenten supersnel "
        "en accuraat om te zetten naar Markdown."
    )
    
    st.subheader("Lokale Opslag")
    st.info(
        f"- **Resultaten:** `{OUTPUT_DIR.resolve()}`\n"
        f"- **Verwerkte PDF's:** `{PROCESSED_DIR.resolve()}`"
    )

    if st.button("Geschiedenis Wissen"):
        st.session_state["processed_results"] = []
        st.success("Verwerkingsgeschiedenis gewist!")
        st.rerun()

# Layout split: Upload vs Preview & Download
col_upload, col_preview = st.columns([1, 1], gap="medium")

with col_upload:
    st.header("1. Documenten Uploaden")
    uploaded_files = st.file_uploader(
        "Upload hier je PDF-bestanden",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:
        st.info(f"{len(uploaded_files)} bestand(en) geselecteerd.")
        
        if st.button("Start Verwerking", type="primary"):
            st.session_state["processed_results"] = []  # Clear previous run results
            
            progress_bar = st.progress(0)
            for index, uploaded_file in enumerate(uploaded_files):
                filename = uploaded_file.name
                
                with st.spinner(f"Bezig met verwerken: {filename}..."):
                    try:
                        # 1. Read bytes from Streamlit
                        pdf_bytes = uploaded_file.getvalue()
                        
                        # 2. Parse using LiteParse in-memory
                        parser = LiteParse(output_format="markdown")
                        result = parser.parse(pdf_bytes)
                        markdown_text = result.text

                        # 3. Save PDF backup to processed/
                        processed_path = PROCESSED_DIR / filename
                        if processed_path.exists():
                            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                            processed_name = f"{Path(filename).stem}_{timestamp}{Path(filename).suffix}"
                            processed_path = PROCESSED_DIR / processed_name
                        processed_path.write_bytes(pdf_bytes)

                        # 4. Save Markdown output to output/
                        output_filename = make_output_filename(filename)
                        output_path = OUTPUT_DIR / output_filename
                        output_path.write_text(markdown_text, encoding="utf-8")

                        # 5. Store in session state
                        st.session_state["processed_results"].append({
                            "original_name": filename,
                            "markdown_name": output_filename,
                            "markdown_text": markdown_text,
                            "status": "success"
                        })
                        
                    except Exception as e:
                        st.error(f"Fout bij verwerken van {filename}: {str(e)}")
                        st.session_state["processed_results"].append({
                            "original_name": filename,
                            "markdown_name": None,
                            "markdown_text": None,
                            "status": "failed",
                            "error": str(e)
                        })
                
                # Update progress bar
                progress_bar.progress((index + 1) / len(uploaded_files))
            
            st.success("Verwerking voltooid!")

with col_preview:
    st.header("2. Resultaten & Downloads")
    
    results = st.session_state["processed_results"]
    
    if not results:
        st.info("Upload bestanden aan de linkerkant en klik op 'Start Verwerking' om resultaten te zien.")
    else:
        successful_results = [r for r in results if r["status"] == "success"]
        
        if successful_results:
            # Batch download as ZIP if there are multiple successful conversions
            if len(successful_results) > 1:
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                    for res in successful_results:
                        zip_file.writestr(res["markdown_name"], res["markdown_text"])
                
                st.download_button(
                    label="🎁 Download Alle Bestanden (ZIP)",
                    data=zip_buffer.getvalue(),
                    file_name=f"parsed_documents_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                    mime="application/zip",
                    use_container_width=True
                )
                st.divider()

            # Individual results display
            for res in results:
                if res["status"] == "success":
                    with st.expander(f"📄 {res['original_name']} ➔ {res['markdown_name']}", expanded=True):
                        # Download button for this specific file
                        st.download_button(
                            label=f"Download {res['markdown_name']}",
                            data=res["markdown_text"],
                            file_name=res["markdown_name"],
                            mime="text/markdown",
                            key=f"dl_{res['markdown_name']}"  # unique key
                        )
                        
                        # Markdown preview
                        st.subheader("Preview:")
                        st.text_area(
                            label="Raw Markdown Content",
                            value=res["markdown_text"],
                            height=200,
                            disabled=True,
                            key=f"preview_{res['markdown_name']}",
                            label_visibility="collapsed"
                        )
                else:
                    st.error(f"❌ {res['original_name']} - Verwerking mislukt: {res['error']}")
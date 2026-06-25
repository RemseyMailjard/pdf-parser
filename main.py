import streamlit as st
import re

DEVELOPER_NAME = "Remsey Mailjard"
DEVELOPER_WEBSITE = "https://www.remsey.nl"

st.set_page_config(
    page_title="YouTube to Transcript",
    page_icon="▶️",
    layout="centered",
)

LANGUAGES = {
    "en": "English",
    "nl": "Dutch (Nederlands)",
    "de": "German (Deutsch)",
    "fr": "French (Français)",
    "es": "Spanish (Español)",
    "pt": "Portuguese (Português)",
    "it": "Italian (Italiano)",
    "ja": "Japanese (日本語)",
    "ko": "Korean (한국어)",
    "zh-Hans": "Chinese Simplified (中文)",
    "ar": "Arabic (العربية)",
    "hi": "Hindi (हिन्दी)",
    "ru": "Russian (Русский)",
    "tr": "Turkish (Türkçe)",
    "pl": "Polish (Polski)",
    "sv": "Swedish (Svenska)",
}

st.markdown(
    """
    <style>
    /* ── Kill Streamlit chrome & top whitespace ── */
    header[data-testid="stHeader"] { display: none !important; height: 0 !important; min-height: 0 !important; }
    #MainMenu { display: none !important; }
    footer { display: none !important; }
    .stAppDeployButton { display: none !important; }

    html, body, .stApp {
        margin: 0 !important;
        padding: 0 !important;
    }

    .stApp > div:first-child { padding-top: 0 !important; margin-top: 0 !important; }
    .stMainBlockContainer,
    [data-testid="stAppViewBlockContainer"],
    .block-container,
    section[data-testid="stMain"],
    section[data-testid="stMain"] > div,
    [data-testid="stVerticalBlock"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    .block-container {
        max-width: 780px !important;
    }

    /* ── Red banner ── */
    .yt-banner {
        background: #ff0000;
        padding: 3.5rem 2rem 2.8rem 2rem;
        text-align: center;
        margin: -2rem -1rem 0 -1rem;
    }
    .yt-banner h1 {
        color: #ffffff !important;
        font-size: 2.8rem;
        font-weight: 900;
        margin: 0 0 0.8rem 0;
        line-height: 1.15;
    }
    .yt-banner p {
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 1.05rem;
        margin: 0.2rem 0;
        font-weight: 400;
    }

    /* ── Tab bar ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        border-bottom: 1px solid #e5e7eb;
        background: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: auto;
        padding: 0.8rem 1.4rem;
        background: transparent !important;
        border: none;
        color: #6b7280 !important;
        font-size: 0.95rem;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        color: #111827 !important;
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #ff0000 !important;
        height: 3px !important;
    }
    .stTabs [data-baseweb="tab-border"] {
        display: none;
    }

    /* ── Primary button → red ── */
    .stButton > button[kind="primary"],
    button[data-testid="stBaseButton-primary"] {
        background-color: #ff0000 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        white-space: nowrap !important;
    }
    .stButton > button[kind="primary"]:hover,
    button[data-testid="stBaseButton-primary"]:hover {
        background-color: #d40000 !important;
    }
    .stButton > button[kind="primary"]:active,
    button[data-testid="stBaseButton-primary"]:active {
        background-color: #b30000 !important;
    }

    /* ── Secondary / download buttons ── */
    .stDownloadButton > button {
        border-color: #ff0000 !important;
        color: #ff0000 !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
    }
    .stDownloadButton > button:hover {
        background-color: #fff5f5 !important;
    }

    /* ── Expander ── */
    [data-testid="stExpander"] {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
    }
    [data-testid="stExpander"] summary span {
        font-weight: 500;
        color: #374151;
    }

    /* ── Text input ── */
    .stTextInput input {
        border-radius: 8px !important;
        border: 1px solid #d1d5db !important;
        padding: 0.65rem 0.9rem !important;
        font-size: 0.95rem !important;
    }
    .stTextInput input:focus {
        border-color: #ff0000 !important;
        box-shadow: 0 0 0 1px #ff0000 !important;
    }

    /* ── Copy button ── */
    .copy-btn {
        display: inline-block;
        padding: 0.5rem 1.2rem;
        background: #f3f4f6;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        color: #374151;
        font-weight: 600;
        font-size: 0.85rem;
        cursor: pointer;
        text-decoration: none;
    }

    /* ── Footer ── */
    .yt-footer {
        text-align: center;
        padding: 2rem 1.5rem 2.5rem 1.5rem;
        border-top: 1px solid #e5e7eb;
        margin-top: 4rem;
    }
    .yt-footer-name {
        font-size: 0.95rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 0.5rem;
    }
    .yt-footer-links {
        display: flex;
        justify-content: center;
        gap: 1.2rem;
        margin-top: 0.6rem;
    }
    .yt-footer-links a {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        color: #6b7280;
        font-size: 0.82rem;
        font-weight: 500;
        text-decoration: none;
        transition: color 0.2s;
    }
    .yt-footer-links a:hover {
        color: #dc2626;
    }

    /* ── Transcript result area ── */
    .stTextArea textarea {
        border-radius: 8px !important;
        border: 1px solid #d1d5db !important;
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif !important;
        font-size: 0.9rem !important;
        line-height: 1.6 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Banner ──
st.markdown(
    """
    <div class="yt-banner">
        <h1>YouTube to Transcript</h1>
        <p>Generate YouTube Transcript for FREE.</p>
        <p>Access all Transcript Languages, Easy Copy and Edit!</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Session state ──
if "transcript_result" not in st.session_state:
    st.session_state["transcript_result"] = None
if "transcript_video_id" not in st.session_state:
    st.session_state["transcript_video_id"] = None
if "available_languages" not in st.session_state:
    st.session_state["available_languages"] = None


def extract_video_id(url: str) -> str | None:
    url = url.strip()
    if re.match(r"^[0-9A-Za-z_-]{11}$", url):
        return url
    patterns = [
        r"(?:v=)([0-9A-Za-z_-]{11})",
        r"(?:youtu\.be/)([0-9A-Za-z_-]{11})",
        r"(?:embed/)([0-9A-Za-z_-]{11})",
        r"(?:shorts/)([0-9A-Za-z_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def format_timestamp(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h > 0:
        return f"{h:d}:{m:02d}:{s:02d}"
    return f"{m:d}:{s:02d}"


def format_srt_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def format_transcript(entries, fmt: str) -> str:
    if fmt == "text":
        return "\n".join(entry["text"] for entry in entries)
    elif fmt == "timestamps":
        return "\n".join(
            f"[{format_timestamp(entry['start'])}] {entry['text']}"
            for entry in entries
        )
    else:
        lines = []
        for i, entry in enumerate(entries, 1):
            start = entry["start"]
            end = start + entry.get("duration", 0)
            lines.append(str(i))
            lines.append(f"{format_srt_time(start)} --> {format_srt_time(end)}")
            lines.append(entry["text"])
            lines.append("")
        return "\n".join(lines)


# ── Tabs ──
tab_transcript, tab_search, tab_channel, tab_playlist, tab_api = st.tabs(
    ["Transcript", "Search", "Channel", "Playlist", "API Docs"]
)

with tab_transcript:
    st.markdown("#### Get Transcript")

    col_url, col_btn = st.columns([5, 1])
    with col_url:
        url = st.text_input(
            "YouTube URL",
            placeholder="Paste YouTube URL here...",
            label_visibility="collapsed",
        )
    with col_btn:
        fetch_clicked = st.button(
            "Get Transcript", type="primary", use_container_width=True
        )

    with st.expander("Language & format options"):
        opt_col1, opt_col2 = st.columns(2)
        with opt_col1:
            lang_codes = list(LANGUAGES.keys())
            language = st.selectbox(
                "Language",
                lang_codes,
                format_func=lambda c: LANGUAGES[c],
            )
        with opt_col2:
            format_option = st.selectbox(
                "Format",
                ["text", "timestamps", "srt"],
                format_func=lambda x: {
                    "text": "Plain Text",
                    "timestamps": "With Timestamps",
                    "srt": "SRT Subtitles",
                }[x],
            )

    if fetch_clicked and url:
        video_id = extract_video_id(url)
        if not video_id:
            st.error("Invalid YouTube URL. Please paste a valid YouTube video link.")
        else:
            with st.spinner("Fetching transcript..."):
                try:
                    from youtube_transcript_api import YouTubeTranscriptApi

                    api = YouTubeTranscriptApi()

                    transcript_list = api.list(video_id)
                    available = {t.language_code: t.language for t in transcript_list}
                    st.session_state["available_languages"] = available

                    try:
                        fetched = transcript_list.find_transcript([language]).fetch()
                    except Exception:
                        try:
                            fetched = transcript_list.find_transcript(["en"]).fetch()
                            st.warning(
                                f"Transcript not available in {LANGUAGES.get(language, language)}. "
                                "Showing English instead."
                            )
                        except Exception:
                            first = next(iter(transcript_list))
                            fetched = first.fetch()
                            st.warning(
                                f"Showing available transcript: {first.language}"
                            )

                    entries = [
                        {"text": s.text, "start": s.start, "duration": s.duration}
                        for s in fetched
                    ]
                    result = format_transcript(entries, format_option)

                    st.session_state["transcript_result"] = result
                    st.session_state["transcript_video_id"] = video_id

                except Exception as e:
                    st.error(f"Could not fetch transcript: {e}")
                    st.session_state["transcript_result"] = None

    elif fetch_clicked:
        st.warning("Please paste a YouTube URL first.")

    if st.session_state["transcript_result"]:
        result = st.session_state["transcript_result"]
        vid = st.session_state["transcript_video_id"]

        if st.session_state.get("available_languages"):
            langs = st.session_state["available_languages"]
            lang_str = ", ".join(f"{name} ({code})" for code, name in langs.items())
            st.caption(f"Available languages: {lang_str}")

        st.text_area(
            "Transcript output",
            value=result,
            height=400,
            label_visibility="collapsed",
        )

        dl_col1, dl_col2 = st.columns([1, 1])
        with dl_col1:
            ext = "srt" if format_option == "srt" else "txt"
            st.download_button(
                label=f"Download .{ext}",
                data=result,
                file_name=f"transcript_{vid}.{ext}",
                mime="text/plain",
                use_container_width=True,
            )
        with dl_col2:
            st.download_button(
                label="Download .md",
                data=result,
                file_name=f"transcript_{vid}.md",
                mime="text/markdown",
                use_container_width=True,
            )


with tab_search:
    st.markdown("#### Search YouTube")
    search_query = st.text_input(
        "Search",
        placeholder="Search for YouTube videos...",
        label_visibility="collapsed",
        key="search_input",
    )
    st.info(
        "Search for YouTube videos and fetch their transcripts. "
        "This feature is coming soon."
    )

with tab_channel:
    st.markdown("#### Channel Transcripts")
    channel_url = st.text_input(
        "Channel URL",
        placeholder="Paste YouTube channel URL...",
        label_visibility="collapsed",
        key="channel_input",
    )
    st.info(
        "Batch-fetch transcripts for all videos in a YouTube channel. "
        "This feature is coming soon."
    )

with tab_playlist:
    st.markdown("#### Playlist Transcripts")
    playlist_url = st.text_input(
        "Playlist URL",
        placeholder="Paste YouTube playlist URL...",
        label_visibility="collapsed",
        key="playlist_input",
    )
    st.info(
        "Batch-fetch transcripts for all videos in a YouTube playlist. "
        "This feature is coming soon."
    )

with tab_api:
    st.markdown("#### API Documentation")
    st.markdown(
        """
**Base URL:** `/api/v1`

**Get Transcript**
```
GET /api/v1/transcript?url={youtube_url}&lang={language_code}&format={text|timestamps|srt}
```

**Parameters:**
| Parameter | Type   | Default | Description                        |
|-----------|--------|---------|------------------------------------|
| `url`     | string | —       | YouTube video URL or video ID      |
| `lang`    | string | `en`    | Language code (e.g. `en`, `nl`)    |
| `format`  | string | `text`  | Output format: `text`, `timestamps`, `srt` |

**Example Response (text):**
```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "en",
  "transcript": "We're no strangers to love..."
}
```

**List Available Languages**
```
GET /api/v1/languages?url={youtube_url}
```

> Full API access coming soon. For now, use the Transcript tab above.
        """
    )

# ── Footer ──
st.markdown(
    f"""
    <div class="yt-footer">
        <div class="yt-footer-name">Built by {DEVELOPER_NAME}</div>
        <div class="yt-footer-links">
            <a href="{DEVELOPER_WEBSITE}" target="_blank">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
                remsey.nl
            </a>
            <a href="https://www.linkedin.com/in/remseymailjard/" target="_blank">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                LinkedIn
            </a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

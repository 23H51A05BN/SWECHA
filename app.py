import streamlit as st
from utils.chapter_loader import load_chapter, get_shloka
from utils.audio import play_audio 

if 'current_shloka' not in st.session_state:
    st.session_state.current_shloka = None

def display_shloka(chapter_num, shloka_num):
    try:
        chapter_data = load_chapter(chapter_num)
        if not chapter_data:
            st.error("అధ్యాయం డేటా లోడ్ కాలేదు")
            return
        
        shloka = get_shloka(chapter_data, shloka_num)
        if not shloka:
            available = [sh.get("verse_number") for sh in chapter_data]
            st.error(f"శ్లోకం {shloka_num} కనుగొనబడలేదు (అందుబాటులో ఉన్నవి: {', '.join(map(str, available))})")
            return

        st.header(f"అధ్యాయం {chapter_num}, శ్లోకం {shloka_num}")
        
        if shloka.get("sloka_audio"):
            play_audio(shloka["sloka_audio"])
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("శ్లోకం")
            st.write(shloka.get("sloka_telugu", ""))
        with col2:
            st.subheader("అనువాదం")
            st.write(shloka.get("translation_telugu", ""))
        
        st.subheader("అర్థం")
        st.write(shloka.get("meaning_telugu", ""))
        
        st.subheader("సారాంశం")
        st.write(shloka.get("summary_telugu", ""))
        
        st.session_state.current_shloka = shloka

    except Exception as e:
        st.error(f"దోషం: {str(e)}")
        st.exception(e)

shloka_num = None
with st.sidebar:
    st.header("భగవద్గీత")
    chapter_num = st.selectbox(
        "అధ్యాయం ఎంచుకోండి",
        options=list(range(1, 19)),
        format_func=lambda x: f"అధ్యాయం {x}"
    )
    chapter_data = load_chapter(chapter_num)
    if chapter_data:
        shloka_options = [sh.get("verse_number") for sh in chapter_data]
        shloka_num = st.selectbox(
            "శ్లోకం",
            options=shloka_options,
            format_func=lambda x: f"శ్లోకం {x}"
        )
        st.markdown("<style>.ai-summary-btn {display: flex; align-items: center;} .ai-summary-btn svg {margin-right: 6px;}</style>", unsafe_allow_html=True)
        btn_label = f"🧠 AI Summary (Chapter {chapter_num})"
        if st.button(btn_label, key=f"ai_summary_ch{chapter_num}"):
            # Collect all summaries from the selected chapter
            summaries = [sh.get("summary_telugu", "") for sh in chapter_data if sh.get("summary_telugu")]
            full_text = " ".join(summaries)
            # Truncate to ~300 words
            words = full_text.split()
            summary_300 = " ".join(words[:300]) + ("..." if len(words) > 300 else "")
            st.info(f"AI Summary (300 words):\n{summary_300}")

if chapter_num and shloka_num:
    display_shloka(chapter_num, shloka_num)

st.sidebar.markdown("---")
st.sidebar.caption(f"Loaded: Chapter {chapter_num}, Shloka {shloka_num}")
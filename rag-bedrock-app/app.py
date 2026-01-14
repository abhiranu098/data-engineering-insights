import streamlit as st
from rag_utils import *

st.set_page_config(
    page_title="GenAI Document Intelligence",
    page_icon="🧠",
    layout="wide"
)

# ---------- SIDEBAR ----------
st.sidebar.title("📁 Upload Documents")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF / CSV / PPT",
    type=["pdf", "csv", "pptx"],
    accept_multiple_files=True
)

mode = st.sidebar.radio(
    "Select Mode",
    ["Ask Questions", "Compare Documents"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Powered by Amazon Bedrock")

# ---------- MAIN TITLE ----------
st.title("🧠 GenAI Document Intelligence Platform")
st.write("Ask questions, compare documents, and extract insights using Amazon Bedrock")

# ---------- FILE INGESTION ----------
all_chunks = []

if uploaded_files:
    for file in uploaded_files:
        if file.name.endswith(".pdf"):
            text = read_pdf(file)
            chunks = [{"chunk": c, "source": file.name} for c in chunk_text(text)]

        elif file.name.endswith(".csv"):
            text = read_csv(file)
            chunks = [{"chunk": c, "source": file.name} for c in chunk_text(text)]

        elif file.name.endswith(".pptx"):
            slides = read_ppt(file)
            chunks = build_chunks_from_ppt(slides, file.name)

        all_chunks.extend(chunks)

    st.success(f"{len(uploaded_files)} file(s) ingested successfully")

    with st.spinner("Building semantic index..."):
        index = build_vector_store(all_chunks)

# ---------- TABS ----------
tab1, tab2, tab3 = st.tabs(["❓ Ask", "🆚 Compare", "ℹ️ Info"])

# ---------- ASK TAB ----------
with tab1:
    st.subheader("Ask a Question")
    question = st.text_input("Enter your question")

    if question:
        with st.spinner("Thinking..."):
            context = retrieve(question, all_chunks, index)
            answer = ask_claude(question, context)

        st.markdown("### ✅ Answer")
        st.write(answer)

        with st.expander("📚 Sources"):
            for c in context:
                st.markdown(f"- {c['source']}")

# ---------- COMPARE TAB ----------
with tab2:
    st.subheader("Compare Documents")

    if len(uploaded_files) < 2:
        st.warning("Upload at least 2 documents to compare")
    else:
        compare_question = st.text_area(
            "What do you want to compare?",
            placeholder="Compare key differences, missing topics, or overlaps"
        )

        if compare_question:
            with st.spinner("Comparing documents..."):
                context = retrieve(compare_question, all_chunks, index)
                answer = ask_claude(compare_question, context)

            st.markdown("### 🆚 Comparison Result")
            st.write(answer)

# ---------- INFO TAB ----------
with tab3:
    st.markdown("""
### ℹ️ About This App

- Built using **Amazon Bedrock (Claude + Titan)**
- Supports **PDF, CSV, PPT**
- Uses **FAISS** for vector search
- Prevents hallucinations
- Slide-level PPT understanding

**Use cases:**
- PPT vs PPT comparison
- Policy change detection
- Document QA
- Knowledge assistant
""")

import streamlit as st
from crawler import crawl_website
from text_processor import split_text
from rag_pipeline import RAGPipeline

st.title("🌐 Website RAG Chatbot")

url = st.text_input("Enter Website URL")

if "pipeline" not in st.session_state:
    st.session_state.pipeline = None

if st.button("Process Website"):
    with st.spinner("Crawling website..."):
        raw_text = crawl_website(url)

    with open("data/raw_text.txt", "w", encoding="utf-8") as f:
        f.write(raw_text)

    chunks = split_text(raw_text)

    pipeline = RAGPipeline()
    pipeline.build(chunks)

    st.session_state.pipeline = pipeline

    st.success("Website processed successfully!")

query = st.text_input("Ask a question")

if st.button("Get Answer"):
    if st.session_state.pipeline:
        answer, sources = st.session_state.pipeline.query(query)

        st.subheader("Answer")
        st.write(answer)

        st.subheader("Sources (Citation)")
        for s in sources:
            st.write(s[:300] + "...")
    else:
        st.warning("Please process a website first.")
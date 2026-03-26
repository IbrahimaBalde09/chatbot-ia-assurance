import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import streamlit as st
from core.rag_pipeline import RAGPipeline

st.set_page_config(page_title="Chatbot IA Assurance", layout="wide")
st.title("Chatbot IA Assurance")
st.write("Pose une question sur les garanties, les sinistres et les démarches d'assurance.")

@st.cache_resource
def load_pipeline():
    return RAGPipeline()

pipeline = load_pipeline()

query = st.text_input("Votre question :")

if query:
    with st.spinner("Recherche et génération de la réponse..."):
        result = pipeline.run(query)

    st.subheader("Réponse du chatbot")
    st.write(result["answer"])

    with st.expander("Sources utilisées"):
        for i, source in enumerate(result["sources"], start=1):
            st.markdown(f"### Source {i}")
            st.write(f"**Fichier :** {source['source']}")
            st.write(source["text"])
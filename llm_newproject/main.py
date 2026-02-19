import os
import streamlit as st

from engine.loader import load_all_policies
from engine.splitter import split_documents
from engine.embeddings import get_embedding_model
from engine.vector_store import get_vector_store, load_vector_store
from engine.retriever import retrieve_documents
from engine.llm import get_llm
from engine.scorer import calculate_risk
from engine.decision_engine import decide_action
from engine.enforcement import enforce

# ----------------------------------------
# Streamlit Config
# ----------------------------------------
st.set_page_config(page_title="RAG Guard Elite", layout="wide")
st.title("🛡 RAG Guard Elite - Secure AI System")

# ----------------------------------------
# Load Models (Cached for Speed)
# ----------------------------------------

@st.cache_resource
def initialize_system():
    embedding_model = get_embedding_model()

    # If vector DB does not exist → build it
    if not os.path.exists("vector_db"):
        docs = load_all_policies("data")
        chunks = split_documents(docs)
        vector_store = get_vector_store(chunks, embedding_model)
    else:
        vector_store = load_vector_store(embedding_model)

    llm = get_llm()

    return vector_store, llm


vector_store, llm = initialize_system()

# ----------------------------------------
# User Input
# ----------------------------------------

user_input = st.text_area("Enter your question:")

if st.button("Submit"):

    if not user_input.strip():
        st.warning("Please enter a question.")
        st.stop()

    # ----------------------------------------
    # STEP 1: Risk Check (FAST)
    # ----------------------------------------
    risk = calculate_risk(user_input)
    action = decide_action(risk)

    # Debug (optional)
    # st.write("Risk Score:", risk)

    enforcement_msg = enforce(action)

    if enforcement_msg:
        st.error(enforcement_msg)
        st.stop()   # 🔥 STOP EVERYTHING HERE (prevents slow processing)

    # ----------------------------------------
    # STEP 2: Retrieval (Only if safe)
    # ----------------------------------------
    with st.spinner("Retrieving policies..."):
        docs = retrieve_documents(vector_store, user_input)
        context = "\n\n".join([doc.page_content for doc in docs])

    # ----------------------------------------
    # STEP 3: LLM Generation
    # ----------------------------------------
    with st.spinner("Generating response..."):
        prompt = f"""
You are a secure AI assistant.

Follow these security policies strictly:

{context}

User Question:
{user_input}
"""
        response = llm.invoke(prompt)

    st.success(response.content)

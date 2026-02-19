from langchain_chroma import Chroma

PERSIST_DIR = "vector_db"

def get_vector_store(docs, embedding_model):
    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embedding_model,
        persist_directory=PERSIST_DIR
    )
    vector_store.persist()
    return vector_store

def load_vector_store(embedding_model):
    return Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embedding_model
    )

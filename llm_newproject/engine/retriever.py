def retrieve_documents(vector_store, query, k=5):
    return vector_store.similarity_search(query, k=k)

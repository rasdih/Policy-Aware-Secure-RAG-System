import os
from langchain_community.document_loaders import UnstructuredMarkdownLoader


def load_all_policies(folder_path="data"):
    documents = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".md"):
            path = os.path.join(folder_path, filename)
            loader = UnstructuredMarkdownLoader(path)
            docs = loader.load()

            for doc in docs:
                doc.metadata["source"] = filename

            documents.extend(docs)

    return documents

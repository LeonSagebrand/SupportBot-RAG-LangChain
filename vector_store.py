import chromadb
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from config import OPENAI_API_KEY, CHROMA_COLLECTION_NAME, CHROMA_DB_DIR

def get_chroma_vectorstore(splits):
    chroma_client = chromadb.Client()
    
    embedding_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    vectorstore = Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        client=chroma_client,
        embedding_function=embedding_model,
        persist_directory=CHROMA_DB_DIR
    )

    try:
        # Add document chunks to the vector store
        vectorstore.add_documents(splits)
        vectorstore.persist()
    except Exception as e:
        print(f"Error adding documents to Chroma vectorstore: {e}")
        raise Exception("Failed to add documents to Chroma vectorstore.")

    return vectorstore

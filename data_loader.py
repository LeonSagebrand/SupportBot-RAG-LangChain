from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_and_chunk_web_data():
    urls = [
        "https://github.com/openai/openai-cookbook",
        "https://github.com/openai/openai-python",
        "https://github.com/openai/openai-node",
        "https://github.com/openai/openai-dotnet",
        "https://github.com/openai/openai-python/blob/main/examples/async_demo.py"
    ]

    try:
        # Load documents from the web
        loader = WebBaseLoader(urls)
        web_docs = loader.load()
    except Exception as e:
        print(f"Error loading documents from the web: {e}")
        raise Exception("Failed to load documents from the web.")

    try:
        # Text splitter for chunking data
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunked_docs = text_splitter.split_documents(web_docs)
    except Exception as e:
        print(f"Error splitting documents: {e}")
        raise Exception("Failed to chunk the documents.")

    return chunked_docs
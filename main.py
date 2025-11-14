# main.py
# AI Intern Assignment 1: Kalpit Pvt Ltd
# --- THIS FILE HAS ALL UPDATED IMPORTS (FINAL) ---

import sys
# UPDATED IMPORTS:
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama

# --- IMPORTS UPDATED TO 'langchain_classic' ---
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Define constants for models and persistence
TEXT_FILE_PATH = "speech.txt"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "mistral"
VECTOR_DB_PATH = "./chroma_db"

def load_documents():
    """
    1. Load the provided text file (speech.txt).
    """
    print(f"Loading document from {TEXT_FILE_PATH}...")
    loader = TextLoader(TEXT_FILE_PATH)
    documents = loader.load()
    return documents

def split_documents(documents):
    """
    2. Split the text into manageable chunks.
    """
    print("Splitting documents into chunks...")
    text_splitter = CharacterTextSplitter(
        chunk_size=500,  # Max size of a chunk
        chunk_overlap=50   # Overlap between chunks to maintain context
    )
    texts = text_splitter.split_documents(documents)
    return texts

def create_vector_store(texts):
    """
    3. Create Embeddings and store them in a local vector store.
    """
    print(f"Creating embeddings using '{EMBEDDING_MODEL}'...")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )
    print(f"Creating and persisting vector store (ChromaDB) at {VECTOR_DB_PATH}...")
    db = Chroma.from_documents(
        texts, 
        embeddings,
        persist_directory=VECTOR_DB_PATH
    )
    print("Vector store created successfully.")
    return db

def create_qa_chain():
    """
    4. & 5. Setup the chain to Retrieve and Generate Answers.
    """
    print("Setting up the RAG Q&A chain...")
    
    # Load the persistent vector store
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )
    db = Chroma(
        persist_directory=VECTOR_DB_PATH, 
        embedding_function=embeddings
    )

    # 4. Set up the retriever
    retriever = db.as_retriever(
        search_kwargs={"k": 2} # Retrieve the top 2 relevant chunks
    )
    
    # 5. Set up the LLM
    llm = Ollama(model=LLM_MODEL)
    
    # 6. Create a prompt template
    prompt = ChatPromptTemplate.from_template(
        """Answer the user's question based only on the following context:

        {context}

        Question: {input}
        """
    )
    
    # 7. Create the "stuff" documents chain
    document_chain = create_stuff_documents_chain(llm, prompt)
    
    # 8. Create the retrieval chain
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
    print("Q&A system is ready.")
    return retrieval_chain

def main():
    """
    Main function to run the setup and start the Q&A loop.
    """
    try:
        # --- One-time setup ---
        documents = load_documents()
        texts = split_documents(documents)
        create_vector_store(texts) 
        
        # --- Create the Q&A chain ---
        qa_chain = create_qa_chain()

        print("\n--- Ambedkar Q&A System ---")
        print("Ask a question based on the provided speech. Type 'exit' to quit.")

        # --- Q&A Loop ---
        while True:
            query = input("\nYour Question: ")
            if query.lower() == 'exit':
                print("Exiting...")
                break
            
            if not query.strip():
                print("Please enter a question.")
                continue
            
            try:
                llm_response = qa_chain.invoke({"input": query})
                
                print("\nAnswer:")
                print(llm_response["answer"].strip())

            except Exception as e:
                print(f"Error during question processing: {e}")
                
    except Exception as e:
        print(f"An error occurred during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
# AmbedkarGPT-Intern-Task

**Submission for the Kalpit Pvt. Ltd. — AI Intern Hiring Assignment**

-<img width="1233" height="551" alt="SAMPLE" src="https://github.com/user-attachments/assets/af997b76-02a5-478e-9999-b682a9918e34" />
--

## Project Overview

This project delivers a fully local, command-line Q&A system designed for the Phase 1 – Core Skills Evaluation of the Kalpit Pvt. Ltd. AI Intern selection process.

It implements an end-to-end Retrieval-Augmented Generation (RAG) workflow. The system ingests the provided speech by Dr. B. R. Ambedkar, processes and indexes it in a local vector store, and answers queries strictly from the supplied document.

The entire pipeline runs offline—no API keys, external services, or cloud dependencies.

### Key Features

* **Text Ingestion:** Reads and preprocesses `speech.txt`
* **Vector Embeddings:** Uses `sentence-transformers/all-MiniLM-L6-v2`
* **Local Vector Store:** ChromaDB for storage and retrieval
* **Local LLM:** Ollama with Mistral 7B
* **RAG Flow:** Constructed with LangChain

---

## Technical Stack

* **Language:** Python 3.8+
* **Framework:** LangChain
* **LLM:** Ollama (Mistral 7B)
* **Vector Database:** ChromaDB
* **Embedding Model:** HuggingFace Sentence Transformers

---

## Getting Started

### 1. Install and Configure Ollama

1. Install Ollama from the official website.
2. Pull the Mistral model:

   ```sh
   ollama pull mistral
   ```
3. Ensure Ollama is running.

### 2. Set Up the Project

1. Clone the repository:

   ```sh
   git clone https://github.com/MrCoss/AmbedkarGPT-Intern-Task.git
   cd AmbedkarGPT-Intern-Task
   ```
2. Create and activate a virtual environment:
   **Windows**

   ```sh
   python -m venv venv
   .\venv\Scripts\activate
   ```

   **macOS / Linux**

   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

---

## Running the Application

Execute the system:

```sh
python main.py
```

### First Run

* Loads and chunks `speech.txt`
* Builds embeddings
* Creates a persistent ChromaDB store in `./chroma_db`

### Subsequent Runs

* Automatically loads the existing vector database

---

## Example Interaction

```
--- Ambedkar Q&A System ---
Ask a question based on the provided speech.
Type 'exit' to quit.

Your Question: What is the problem of caste?

Answer: The text explains that the caste problem stems from the belief in the sanctity and authority of the shastras.

Your Question: What is the real remedy?

Answer: The remedy suggested is to challenge and discard the belief in the sanctity of the shastras.

Your Question: exit
Exiting...
```

---

## Project Structure

```
AmbedkarGPT-Intern-Task/
│
├── .gitignore          # Ignores venv, chroma_db, pycache
├── README.md           # Project documentation
├── main.py             # RAG pipeline and CLI logic
├── requirements.txt    # Python dependencies
└── speech.txt          # Source text used for retrieval
```

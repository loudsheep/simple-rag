# 🎓 University RAG Assistant

This is a simple **Retrieval-Augmented Generation (RAG)** system that allows you to ask questions based on your **university files** (tasks, lectures, presentations, code, etc.).  
It uses **Flask**, **LlamaIndex**, **Ollama**, **ChromaDB**, and **HuggingFace** embeddings to answer questions.

---

## 🚀 Features

- Upload your university materials in one folder
- Ask questions about them via an API (`/api/question`)
- Uses LLMs (like `llama2:7b`) and semantic search
- Prompt optimized for Polish academic context

---

## 🧱 Project Structure

```
.
├── api.py               # Flask app (API endpoint)
├── model.py             # LLM + embedding + index + query logic
├── config.py            # Configuration loaded from .env
├── .env                 # Environment variables
├── /docs                # Folder with university documents
└── requirements.txt     # Python dependencies
```

---

## ⚙️ Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd <project-folder>
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Manually install below module to get rid of dependency install issues with `requirements.txt`
```bash
pip install llama-index-vector-stores-chroma
```

### 3. Create `.env` file
Example:

```env
DOCS_DIR=./docs

HTTP_PORT=7654

CHROMA_HOST=localhost
CHROMA_PORT=8000
```

### 4. Prepare your university documents

Put your `.pdf`, `.docx`, `.txt`, `.md`, or `.py` files in the `./docs` folder.

---

## 🧠 Start the Server

```bash
python api.py
```

Then, send a POST request to:

```
POST http://localhost:7654/api/question
```

With JSON body:

```json
{
  "question": "Jak działa algorytm Dijkstry?"
}
```

---

## 💬 CLI Mode

To run it in command-line mode:

```bash
python model.py
```

And ask questions interactively.

---

## 📚 Technologies

- [LlamaIndex](https://llamaindex.ai/)
- [Ollama](https://ollama.com/) (`llama2:7b` used)
- [ChromaDB](https://www.trychroma.com/)
- [Flask](https://flask.palletsprojects.com/)
- [HuggingFace Embeddings](https://huggingface.co/BAAI/bge-small-en-v1.5)

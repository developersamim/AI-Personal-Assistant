# Personal Assistant

A local retrieval-augmented personal assistant. It reads Markdown files from `knowledge-base/`, stores searchable embeddings in Chroma, and uses Ollama to answer questions locally.

## Project Flow

```text
knowledge-base/*.md -> ingest.py -> vector_db/ -> answer.py -> Ollama response
```

## Prerequisites

Install the following:

- Python 3.9 or newer
- Ollama
- Enough disk space and memory for the Ollama model you choose

Download Ollama from [ollama.com](https://ollama.com/download).

## Setup

### 1. Open the project directory

```bash
cd personal_assistant
```

### 2. Create a virtual environment

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install Python dependencies

macOS or Linux:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Windows PowerShell:

```powershell
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

### 4. Start Ollama

Start Ollama if it is not already running:

```bash
ollama serve
```

Keep this terminal open. Use a second terminal for the remaining commands, and activate the virtual environment there as well.

Ollama normally listens at:

```text
http://localhost:11434
```

### 5. Download the chat model

The project is configured to use `gpt-oss:20b`:

```bash
ollama pull gpt-oss:20b
```

Confirm that the model is installed:

```bash
ollama list
```

### 6. Add or update personal knowledge

Put Markdown files in `knowledge-base/`. The existing folders are examples of how content can be organized:

```text
knowledge-base/
├── personal/
│   └── AboutMe.md
└── schools/
    ├── BalMandir School.md
    └── Gautam School.md
```

Add, edit, or remove `.md` files as needed.

### 7. Build the vector database

Run ingestion after the first setup and every time the knowledge-base changes:

```bash
python ingest.py
```

This recreates the local Chroma database in `vector_db/`.

The first run may download the HuggingFace embedding model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

### 8. Ask a question

From the project directory, run:

```bash
python -c 'from answer import answer_question; print(answer_question("What do you know about me?")[0])'
```

For another question:

```bash
python -c 'from answer import answer_question; print(answer_question("Where did I go to school?")[0])'
```

On Windows PowerShell, use:

```powershell
python -c "from answer import answer_question; print(answer_question('What do you know about me?')[0])"
```

## Updating the Knowledge Base

1. Edit or add Markdown files under `knowledge-base/`.
2. Run `python ingest.py` to rebuild the vector database.
3. Run the question command again.

Do not skip the ingestion step after changing the knowledge base, because `answer.py` reads the existing data in `vector_db/`.

## Troubleshooting

### Ollama connection error

Make sure Ollama is running and listening on port `11434`:

```bash
ollama serve
```

### Model not found

Pull the configured model again:

```bash
ollama pull gpt-oss:20b
```

### No useful answers

Check that the knowledge files are Markdown files under `knowledge-base/`, then rebuild the database:

```bash
python ingest.py
```

### Python package errors

Make sure the virtual environment is active, then reinstall the dependencies:

```bash
python -m pip install -r requirements.txt
```

### Existing vector database is stale

Run ingestion again. The ingestion script deletes and recreates the Chroma collection:

```bash
python ingest.py
```

## Main Files

- `ingest.py`: loads Markdown files, splits them into chunks, creates embeddings, and rebuilds Chroma.
- `answer.py`: retrieves relevant chunks and asks the local Ollama model for an answer.
- `requirements.txt`: Python dependencies.
- `knowledge-base/`: personal Markdown source files.
- `vector_db/`: generated local vector database.

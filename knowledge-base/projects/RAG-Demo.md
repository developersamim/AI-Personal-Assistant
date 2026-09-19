# RAG Demo Project

This is fictional demo data about the project.

- **Project name:** Personal Assistant
- **Architecture:** Markdown knowledge base -> HuggingFace embeddings -> Chroma vector database -> Ollama chat model
- **Retrieval step:** The application searches the most relevant knowledge chunks before generating an answer.
- **Generation step:** Ollama uses the retrieved context to compose a response locally.
- **Why RAG:** The model does not need to memorize Alex's details. It can look them up from the knowledge base at question time.
- **Privacy angle:** The demo is designed to run locally, so the sample facts stay on the developer's computer.
- **Known limitation:** If a fact is not in the knowledge base, the assistant should admit that it does not know instead of improvising a biography.

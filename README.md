# Runbook Assistant

A retrieval-augmented runbook assistant helps you with following
- Incident response and troubleshooting
- Searching runbooks and technical documentation
- Searching code, architecture decisions, and past incidents

## macOS Setup with uv

Install `uv` if it is not already installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Open the project directory:

```bash
cd personal_assistant
```

Install the dependencies:

```bash
uv sync
```

`uv` uses `pyproject.toml` as the project configuration file. It reads the dependency list from `pyproject.toml` and records resolved versions in `uv.lock`. Do not use `pip` or manage a separate dependency list for this project.

### Optional requirements.txt Installation

`requirements.txt` is optional and is provided for environments such as deployment services that expect a requirements file. The recommended local workflow is still `uv sync`, which uses `pyproject.toml` and `uv.lock`.

To install the packages from `requirements.txt` with `uv`, run:

```bash
uv pip install -r requirements.txt
```

This installs the listed packages into the active environment, but it does not update `pyproject.toml` or `uv.lock`. Use `uv add package-name` when adding a project dependency so the project configuration stays up to date.

Run document ingestion:

```bash
uv run python ingest.py
```

Run the application:

```bash
uv run python app.py
```

## Managing Libraries with uv

Add a library:

```bash
uv add package-name
```

For example:

```bash
uv add langchain-pinecone
```

`uv add` updates `pyproject.toml`, updates `uv.lock`, and installs the library into the project environment.

## Updating Packages with uv

Update one package to the newest version allowed by its version rule in `pyproject.toml`:

```bash
uv lock --upgrade-package package-name
uv sync
```

For example:

```bash
uv lock --upgrade-package langchain-pinecone
uv sync
```

To change the version rule and update the package at the same time, use `uv add`:

```bash
uv add 'langchain-pinecone>=0.2.0'
```

To upgrade all packages within their allowed version ranges:

```bash
uv lock --upgrade
uv sync
```

Review the changes to `pyproject.toml` and `uv.lock` after upgrading packages. If an upgrade causes compatibility problems, restore the previous dependency rule and synchronize the environment again.

Remove a library:

```bash
uv remove package-name
```

For example:

```bash
uv remove langchain-chroma
```

After changing dependencies manually in `pyproject.toml`, synchronize the environment with:

```bash
uv sync
```

## Why Specific Package Versions Are Used

The dependency rules in `pyproject.toml` use exact versions, minimum versions, or upper bounds depending on the package:

- `gradio>=5.0,<6` keeps the application on the Gradio 5 release line. The application depends on Gradio's component and event APIs, so a major-version upgrade could change the UI behavior.
- `pydantic>=2.11.1,<2.12` keeps Pydantic compatible with both the Gradio schema handling and the LangChain Pinecone integration used by this project.
- `langchain-pinecone>=0.2.0` is required because the project uses `PineconeVectorStore` to retrieve and upload vectors.
- `pinecone>=7.0.0,<8.0.0` keeps the Pinecone SDK within the range supported by the selected LangChain Pinecone integration.
- `torch==2.2.2` is pinned because the embedding stack depends on PyTorch and changes to its version can affect installation compatibility and model behavior.
- `sentence-transformers>=3.3,<4` and `transformers>=4.41,<5` keep the embedding libraries on compatible major-version lines.
- `numpy<2` avoids compatibility problems with packages in the machine-learning and embedding stack that may not support NumPy 2.
- `fastapi==0.115.2` and `starlette==0.38.6` keep the web framework components aligned with the application environment.
- `onnxruntime==1.19.2` is pinned for compatibility with the installed Python and embedding dependencies.
- `requires-python = ">=3.12,<3.13"` keeps the project on Python 3.12, which matches the tested dependency environment.

These constraints allow `uv` to resolve a compatible environment while `uv.lock` records the exact versions installed. Update packages deliberately rather than removing version bounds without checking compatibility.

Run ingestion again whenever the files under `knowledge-base/` change.

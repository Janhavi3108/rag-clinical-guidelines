# RAG over Cervical Cancer Guidelines

A retrieval-augmented question answering system over public cervical cancer
guidelines, with a measured retrieval and answer evaluation. Everything runs
on free, open-source tools.

**Status:** work in progress (Day 1 of 21: setup done)

## Goal
Answer questions about cervical cancer screening and management using only
the source documents, cite the file and page, and say "not found" when the
documents don't contain the answer.

## Sources
Three public documents (WHO 2021 guideline, ICMR 2016 consensus document,
MoHFW 2016 operational framework). Links and licences are in
[SOURCES.md](SOURCES.md). The PDFs are not stored in this repo.

## Stack
- Embeddings: BAAI/bge-small-en-v1.5
- Vector search: FAISS
- Generator: qwen2.5:3b via Ollama (about 7.5 tokens/s on an 8 GB CPU-only laptop)
- Demo: Gradio on Hugging Face Spaces (planned)

## Setup
1. Clone the repo and create a virtual environment.
2. `pip install -r requirements.txt`
3. Download the PDFs from SOURCES.md into a local `data/` folder.
4. Install Ollama and run `ollama pull qwen2.5:3b`.

## Disclaimer
Not medical advice. This is a learning project and may give wrong answers.
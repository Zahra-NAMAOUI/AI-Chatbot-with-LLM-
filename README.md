# 🤖 AI Chatbot with LLM & RAG

A conversational AI chatbot built with **FastAPI** and **Ollama**, 
running a local LLM (smollm:135m) with a clean web interface.

![Chatbot Screenshot](screenshot.png)

---

## 🚀 Features

- Local LLM inference using Ollama (no API key needed)
- REST API built with FastAPI
- Clean chat web interface with dark/light theme
- Switch between models dynamically
- Containerized deployment with Docker

---

## 🛠️ Tech Stack

- **Python** — core language
- **FastAPI** — REST API framework
- **Ollama** — local LLM runner
- **Docker** — containerized deployment
- **smollm:135m** — lightweight LLM model

---

## ⚙️ How to Run

### Option 1 — Without Docker

1. Install [Ollama](https://ollama.com) and pull the model:
```bash
   ollama pull smollm:135m
```

2. Install dependencies:
```bash
   pip install -r app/requirements.txt
```

3. Run the app:
```bash
   uvicorn app.app:app --host 0.0.0.0 --port 8000
```

4. Open browser at:

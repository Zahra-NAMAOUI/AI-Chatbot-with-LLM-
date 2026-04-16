# 🤖 AI Chatbot with LLM & RAG

A conversational AI chatbot built with **FastAPI** and **Ollama**, 
running a local LLM (smollm:135m) with a clean web interface.

![Chatbot Screenshot](chat.jpg)

---

## 🚀 Features

- Local LLM inference using Ollama (no API key needed)
- REST API built with FastAPI
- Clean chat web interface with dark/light theme
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
```bash
   http://localhost:8000/test
```
### Option 2 — With Docker

```bash
docker compose up
```
Then open `http://localhost:8000/test`

---

## 📡 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /test` | Chat web interface |
| `GET /chat?prompt=...` | Send a message to the LLM |
| `GET /model-info` | Get current model info |
| `GET /switch-model?new_model=...` | Switch LLM model |
| `GET /about` | About page |

---

## 👩‍💻 Author

**Fatimazahra Namaoui** — Data & AI Engineering Student  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/fz-namaoui)

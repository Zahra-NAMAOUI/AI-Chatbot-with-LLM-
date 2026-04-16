from fastapi import FastAPI
from fastapi.responses import HTMLResponse  # Correction ici
import ollama
from fastapi.responses import JSONResponse

app = FastAPI()
MODEL_NAME = "smollm:135m"  # Variable globale pour le modèle actuel

@app.get("/chat")
async def chat(prompt: str):
    try:
        response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}])
        return {"response": response['message']['content']}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/model-info")
async def model_info():
    try:
        models = ollama.list()
        print("Models response:", models)  # Débogage
        if 'models' in models and isinstance(models['models'], list):
            for model in models['models']:
                if hasattr(model, 'model') and model.model.lower() == MODEL_NAME.lower():
                    return {
                        "model_name": model.model,
                        "details": {
                            "size": getattr(model, 'size', 'N/A'),
                            "status": "available"
                        }
                    }
        return JSONResponse(status_code=404, content={"error": f"Model {MODEL_NAME} not found"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/switch-model")
async def switch_model(new_model: str):
    global MODEL_NAME
    try:
        models = ollama.list()
        if 'models' in models and isinstance(models['models'], list):
            for model in models['models']:
                if hasattr(model, 'model') and model.model.lower() == new_model.lower():
                    MODEL_NAME = new_model
                    return {"message": f"Switched to model {MODEL_NAME}"}
        return JSONResponse(status_code=404, content={"error": f"Model {new_model} not found"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/test", response_class=HTMLResponse)
async def test_page():
    html_content = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Mon Chatbot Élégant</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
                margin: 0;
                padding: 20px;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }
            .chat-container {
                background: white;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                width: 600px; /* Plus large */
                max-width: 90%;
                position: relative;
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
            }
            .logo {
                font-size: 24px;
                color: #2c3e50;
                font-weight: bold;
            }
            .theme-btn {
                padding: 8px 15px;
                background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%); /* Bleu foncé dégradé */
                color: white;
                border: none;
                border-radius: 20px;
                cursor: pointer;
                font-size: 14px;
                transition: background 0.3s;
            }
            .theme-btn:hover {
                background: #2c3e50;
            }
            .messages {
                height: 500px; /* Zone plus longue */
                overflow-y: auto;
                background: #f9f9f9;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 20px;
                color: #34495e;
            }
            .message {
                margin: 10px 0;
                padding: 10px;
                background: #ecf0f1;
                border-radius: 5px;
                max-width: 80%;
            }
            .input-area {
                display: flex;
                gap: 10px;
            }
            input[type="text"] {
                flex-grow: 1;
                padding: 12px;
                font-size: 16px;
                border: 1px solid #ddd;
                border-radius: 25px;
                outline: none;
                height: 40px; /* Réduit mais long */
                width: 85%; /* Ajuste la largeur */
            }
            button[type="submit"] {
                padding: 12px 20px;
                background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%); /* Bleu foncé dégradé */
                color: white;
                border: none;
                border-radius: 20px;
                cursor: pointer;
                font-size: 14px;
                width: 80px; /* Plus petit */
                display: flex;
                align-items: center;
                justify-content: center;
            }
            button[type="submit"]:hover {
                background: #2c3e50;
            }
            .dark-theme {
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            }
            .dark-theme .chat-container { background: #1a252f; }
            .dark-theme .logo { color: #ecf0f1; }
            .dark-theme .messages { background: #2f4050; color: #bdc3c7; }
            .dark-theme .message { background: #34495e; }
            .dark-theme input[type="text"] { border-color: #4a6074; background: #2f4050; color: #ecf0f1; }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div class="header">
                <div class="logo">LLM Assistant</div> <!-- Remplace [Ton Nom] -->
                <button class="theme-btn" onclick="toggleTheme()">Le Thème</button>
            </div>
            <div class="messages" id="messages"></div>
            <form class="input-area" action="/chat" method="get">
                <input type="text" id="prompt" name="prompt" required placeholder="Tape ton message...">
                <button type="submit">Envoyer</button>
            </form>
            <script>
                const messagesDiv = document.getElementById('messages');
                document.querySelector('form').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const prompt = document.getElementById('prompt').value;
                    if (prompt) {
                        const messageDiv = document.createElement('div');
                        messageDiv.className = 'message';
                        messageDiv.textContent = `Toi: ${prompt}`;
                        messagesDiv.appendChild(messageDiv);
                        messagesDiv.scrollTop = messagesDiv.scrollHeight;
                        document.getElementById('prompt').value = '';
                        messagesDiv.innerHTML += '<div class="message">Chatbot: Chargement...</div>';
                        const response = await fetch(`/chat?prompt=${encodeURIComponent(prompt)}`);
                        const data = await response.json();
                        const result = data.response || data.error;
                        messagesDiv.removeChild(messagesDiv.lastChild);
                        const botMessageDiv = document.createElement('div');
                        botMessageDiv.className = 'message';
                        botMessageDiv.textContent = `Chatbot: ${result}`;
                        messagesDiv.appendChild(botMessageDiv);
                        messagesDiv.scrollTop = messagesDiv.scrollHeight;
                    }
                });
                function toggleTheme() {
                    document.body.classList.toggle('dark-theme');
                }
            </script>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/about", response_class=HTMLResponse)
async def about_page():
    html_content = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>À propos</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
                margin: 0;
                padding: 20px;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }
            .about-container {
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                width: 500px;
                text-align: center;
            }
            h1 { color: #2c3e50; font-size: 28px; margin-bottom: 20px; }
            p { color: #34495e; font-size: 16px; line-height: 1.6; }
            .logo { font-size: 40px; color: #2ecc71; margin-bottom: 20px; } /* Symbole stylisé */
            a {
                padding: 10px 20px;
                background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
                color: white;
                text-decoration: none;
                border-radius: 20px;
                display: inline-block;
                margin-top: 20px;
            }
            a:hover { background: #2c3e50; }
        </style>
    </head>
    <body>
        <div class="about-container">
            <div class="logo">🌟</div> <!-- Symbole personnalisé, remplace par un logo si tu veux -->
            <h1>À propos de mon Chatbot</h1>
            <p>Créé par Tima</p>
            <p>Cet chatbot utilise FastAPI et Ollama avec une touche élégante et personnelle.</p>
            <a href="/test">Retourner au Chatbot</a>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from chatbot import Chatbot
import uvicorn
import os

app = FastAPI()
chatbot = Chatbot()

# Configuration des templates et des fichiers statiques
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "messages": chatbot.conversation_history})

@app.post("/chat")
async def chat(message: str = Form(...)):
    response = await chatbot.get_response(message)
    return {"response": response}

@app.post("/clear")
async def clear_history():
    chatbot.clear_history()
    return {"status": "success"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

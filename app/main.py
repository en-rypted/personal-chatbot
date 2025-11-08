import gradio as gr
from app.service.chatbot import chat
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
# gr.ChatInterface(chat, type="messages").launch()


history = []
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "WebSocket server is running ✅"}

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    history = []
    try:
        while True:
            # Receive message from client
            user_msg = await websocket.receive_text()
            
            # Simple bot reply (later replace with AI)
            reply, history = chat(user_msg, history)
            # print(history)
            # Send response back to client
            await websocket.send_text(reply)

    except WebSocketDisconnect:
        print("Client disconnected ❌")


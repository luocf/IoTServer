from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.responses import HTMLResponse

from typing import List, Optional

from app.db import engine, Base, init_db
from app.api import superadmin, users, devices, areas, tasks

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()
    
app.include_router(superadmin.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(devices.router, prefix="/api")
app.include_router(areas.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")

# WebSocket connection manager for tracking all connected WebSocket clients
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Broadcast message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        
@app.get("/")
async def get():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>FastAPI WebSocket</title>
    </head>
    <body>
        <h1>WebSocket Client</h1>
        <button onclick="sendMessage()">Send Message</button>
        <ul id='messages'>
        </ul>
        <script>
            const ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                const messages = document.getElementById('messages')
                const message = document.createElement('li')
                const content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };

            function sendMessage() {
                ws.send("Hello, World!");
            }
        </script>
    </body>
    </html>
    """)

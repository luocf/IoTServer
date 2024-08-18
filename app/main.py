from fastapi import FastAPI
from app.db import engine, Base
from app.api import users, spaces, devices

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router, prefix="/api")
app.include_router(spaces.router, prefix="/api")
app.include_router(devices.router, prefix="/api")

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

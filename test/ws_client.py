import asyncio
import websockets

async def websocket_client():
    uri = "ws://localhost:8000/ws"  # 服务器地址
    async with websockets.connect(uri) as websocket:
        # 发送消息到服务器
        await websocket.send("Hello from the client!")

        while True:
            try:
                # 接收服务器的消息
                response = await websocket.recv()
                print(f"Received from server: {response}")
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed by server")
                break

# 运行客户端
if __name__ == "__main__":
    asyncio.run(websocket_client())

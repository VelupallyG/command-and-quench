import asyncio
import websockets
import threading

async def echo_server(websocket):
    print("Server: Client connected")
    try:
        async for message in websocket:
            print(f"Server received: {message}")
            await websocket.send(f"Echo: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("Server: Client disconnected")

def start_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def run_server():
        async with websockets.serve(echo_server, "0.0.0.0", 8765):
            await asyncio.Future()  # Run forever

    loop.run_until_complete(run_server())

# Start server in background thread
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

print("WebSocket server started on ws://localhost:8765")
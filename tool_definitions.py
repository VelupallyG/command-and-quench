import websockets

async def dispense_drink():
    """
    Dispenses a drink can by sending a signal to the microcontroller.
    """
    uri = "ws://localhost:8765"
    try:
        async with websockets.connect(uri) as websocket:
            msg = "Dispense Drink!"
            print(f"📤 Client sending: {msg}")
            await websocket.send(msg)
            response = await websocket.recv()
            print(f"📥 Client received: {response}")
            return True
    except Exception as e:
        print(f"❌ WebSocket error: {e}")
        return False
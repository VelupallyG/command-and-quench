# # tool_definitions.py
# import serial
# import time

# # --- Configuration ---
# # Find your serial port. On Windows it's COMx, on Linux/macOS it's /dev/tty.usbmodemXXXX
# SERIAL_PORT = '/dev/tty.usbmodem14201'  # <-- IMPORTANT: CHANGE THIS
# BAUD_RATE = 9600

# # --- Serial Communication Helper ---
# def send_command_to_mcu(command: str):
#     """Sends a command string to the microcontroller and waits for an acknowledgment."""
#     try:
#         with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as ser:
#             print(f"PYTHON: Sending command: '{command}'")
#             ser.write(f"{command}\n".encode('utf-8'))
            
#             # Wait for acknowledgment
#             response = ser.readline().decode('utf-8').strip()
#             print(f"MCU: Responded with: '{response}'")
#             return response
#     except serial.SerialException as e:
#         print(f"ERROR: Could not connect to {SERIAL_PORT}. Is the device connected?")
#         print(f"Error details: {e}")
#         return f"ERROR: {e}"

# # --- Drink Dispenser Tool ---
# def dispense_drink():
#     """
#     Dispenses a drink can by sending a signal to the microcontroller.
#     """
#     print("DRINK DISPENSER: Dispensing drink can...")
    
#     # Simple command to trigger drink dispensing
#     command = "DISPENSE_DRINK"
    
#     response = send_command_to_mcu(command)
    
#     if "ERROR" not in response:
#         return "✅ Drink can dispensed successfully! Enjoy your drink!"
#     else:
#         return f"❌ Failed to dispense drink: {response}"

# tool_definitions.py
import asyncio
import websockets
import threading
import time

# Configuration
WEBSOCKET_URL = 'ws://localhost:8080'

# Test WebSocket Server
async def test_server(websocket):
    """Simple test server that responds to '1' with dispense confirmation."""
    print("🖥️  Test server: Client connected")
    try:
        async for message in websocket:
            print(f"🖥️  Test server: Received '{message}'")
            if message == "1":
                print("🖥️  Test server: Dispensing drink...")
                await websocket.send("OK")
    except websockets.exceptions.ConnectionClosed:
        print("🖥️  Test server: Client disconnected")

def start_test_server():
    """Start the test WebSocket server in background."""
    print("🖥️  Starting test WebSocket server on port 8080...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    async def run_server():
        async with websockets.serve(test_server, "localhost", 8080):
            await asyncio.Future()  # Run forever
    
    loop.run_until_complete(run_server())

# Client functions
async def dispense_drink():
    """Send '1' to WebSocket to dispense drink."""
    try:
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            await websocket.send("1")
            response = await websocket.recv()
            print(f"✅ MCU responded: {response}")
            return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def dispense():
    """Simple function to dispense a drink."""
    return asyncio.run(dispense_drink())

if __name__ == "__main__":
    # Start test server in background thread
    server_thread = threading.Thread(target=start_test_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    time.sleep(1)
    
    print("📱 Dispensing drink...")
    dispense()
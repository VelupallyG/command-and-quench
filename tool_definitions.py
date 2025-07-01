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

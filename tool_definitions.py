# import websockets

# async def dispense_drink():
#     """
#     Dispenses a drink can by sending a signal to the microcontroller.
#     """
#     uri = "ws://localhost:8765"
#     try:
#         async with websockets.connect(uri) as websocket:
#             msg = "Dispense Drink!"
#             print(f"Client sending: {msg}")
#             await websocket.send(msg)
#             response = await websocket.recv()
#             print(f"Client received: {response}")
#             return True
#     except Exception as e:
#         print(f"WebSocket error: {e}")
#         return False

import serial
import time

def dispense_drink():
    """
    Dispenses a drink can by sending a signal to the microcontroller over serial.

    Args:
        port (str): Serial port device path, e.g., "/dev/ttyUSB0" or "/dev/tty.usbserial"
        baudrate (int): Baud rate for serial communication (must match microcontroller settings)
    
    Returns:
        bool: True if successful, False if error
    """
    port="/dev/tty.usbmodemDC5475C574742"
    baudrate=115200
    try:
        with serial.Serial(port, baudrate, timeout=2) as ser:
            msg = "1\n"  # Send string with newline, Arduino commonly expects this
            print(f"Serial sending: {msg.strip()}")
            ser.write(msg.encode('utf-8'))

            # Wait for Arduino response (optional)
            time.sleep(0.5)
            if ser.in_waiting > 0:
                response = ser.readline().decode('utf-8').strip()
                print(f"Serial received: {response}")
            else:
                print("No response from device.")
            return True
    except Exception as e:
        print(f"Serial communication error: {e}")
        return False
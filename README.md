# Invisible Spy

Invisible Spy is a Python application that captures keyboard input and sends it to a specified server. It uses the `pynput` library to listen for keyboard events and the `aiohttp` library to send HTTP requests asynchronously.

## Features

- Captures all keystrokes and sends them to a server.
- Sends data asynchronously to reduce latency.
- Handles special keys such as Enter, Tab, Space, and Backspace.
- Ignores certain keys like Shift, Ctrl, and Escape.

## Usage

To run the application, execute the `master.py` script. Make sure to configure the IP address, port number, and time interval in the constants section of the script.

## Dependencies

- Python 3.6+
- aiohttp
- pynput

## License

This project is licensed under the MIT License. See the LICENSE file for details.

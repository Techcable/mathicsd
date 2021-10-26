import sys
import time
import requests
from typing import Optional
import webview

from requests.exceptions import RequestException

from . import FatalError, run_server, PORT, server_process, warning, local_storage

URL=f"http://localhost:{PORT}"

def detect_default_backend() -> Optional[str]:
    if sys.platform == 'linux':
        # Combination of pystray + 
        return 'qt'
    try:
        # Surprisingly, Qt has lower memory usage in my tests..
        # This is despite the fact it's backed by chromium
        import PyQt5
        import PyQt5.QtWebEngineWidgets
        return 'qt'
    except ImportError:
        return 'gtk'

def wait_for_server():
    print("Waiting for web-server..")
    while True:
        if server_process() is None:
            raise FatalError("Server process died!")
        try:
            requests.head(URL)
        except RequestException:
            continue
        else:
            print("Successful connection!")
            break

def spawn_webview(backend):
    print(f"Connecting to {URL}")
    webview.create_window("Mathics!", url=URL)
    wait_for_server()
    webview.start(gui=backend)

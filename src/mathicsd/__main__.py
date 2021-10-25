from typing import Optional

import pystray
import click
import webview
import time
import socket
import requests
import sys
from PIL import Image
from threading import Thread

import importlib.resources

from requests.exceptions import RequestException
from . import FatalError, run_server, PORT, server_process, warning, local_storage

URL=f"http://localhost:{PORT}"

def load_logo() -> Image:
    f = importlib.resources.open_binary("mathicsd.resources", "logo.png")
    try:
        img = Image.open(f)
        return img.copy()
    finally:
        f.close()


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

def spawn_icon():
    # NOTE: See below for IDEA TO FIX ALL BUGS!!!
    def run_icon():
        icon = pystray.Icon("Mathics!", load_logo(), backend='gtk')
        icon.run()
    t = Thread(target=run_icon, name="Icon Thread")
    t.start()


@click.command('mathicsd')
@click.option('--backend', default=detect_default_backend(),
    help="Explicitly specify the webview backend to use.")
def run(backend):
    run_server()
    print(f"Connecting to {URL}")
    webview.create_window("Mathics!", url=URL)
        #html=f"""<p>Hello!</p>
        # <iframe src="http://localhost:{PORT}">""")
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
    # IDEA: Spawn a SUBPROCESS to deal with the webview
    # By spawning a subprocess, we can fix the issues with pystray & webview integration
    # Issues like closing apps & messing with GTK context magically disapear.
    # See issue #1
    webview.start(func=spawn_icon, gui=backend)


if __name__ == "__main__":
    run()

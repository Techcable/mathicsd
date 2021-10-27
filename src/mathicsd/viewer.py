import sys
import time
import requests
from typing import Optional
import importlib.resources
from dataclasses import dataclass

import webview

from requests.exceptions import RequestException

from . import FatalError, run_server, PORT, server_process, warning, local_storage, load_svg_logo

URL=f"http://localhost:{PORT}"

@dataclass
class ViewerSettings:
    loading_wait: Optional[float] = None
    show_startup_msg: bool = True
    backend: Optional[str] = None

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

def loading_screen() -> str:
    f = importlib.resources.open_text("mathicsd.resources", "loading.html")
    try:
        text = f.read()
    finally:
        f.close()
    text = text.replace("{{SVG_LOGO}}", load_svg_logo())
    return text

def wait_for_server(window, settings: ViewerSettings):
    if settings.loading_wait is not None:
        print(f"Waiting {settings.loading_wait}s")
        # Gives the user time to see the license (and the server time to boot)
        # Some of the Mathics developers seemed concered about this
        # See Mathics3/mathics-django#142 for discussion
        time.sleep(settings.loading_wait)
    # Verify the server is actually ready...
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
    window.load_url(URL)

def spawn_webview(settings: ViewerSettings):
    print(f"Connecting to {URL}..")
    if not settings.show_startup_msg:
        warning("Suppressing startup message is currently unsupported. See PR Mathics3/mathics-django#142")
    window = webview.create_window("Mathics!", html=loading_screen())
    webview.start(wait_for_server, (window, settings), gui=settings.backend)


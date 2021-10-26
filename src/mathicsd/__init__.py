# PyWebview: https://pywebview.flowrl.com/
import os
import sys
import shutil
import signal
from pathlib import Path
from typing import Optional
from subprocess import Popen, DEVNULL, TimeoutExpired
from threading import Thread

import click
import psutil

PORT = 8571

class FatalError(click.ClickException):
    pass

def warning(*args, **kwargs):
    print("WARNING:", *args, **kwargs, file=sys.stderr)

def local_storage(create=False) -> Path:
    if sys.platform in ("linux", "macos"):
        p = Path(Path.home(), ".local", "share", "mathicsd")
        if create:
            p.mkdir(parents=True, exist_ok=True)
        return p
    else:
        raise FatalError("NYI: Windows ~/.local/share directory")

def process_file(create=False) -> Path:
    return Path(local_storage(create=create), "mathics_server.pid")


_SERVER_PROCESS = None
def server_process() -> Optional[psutil.Process]:
    if _SERVER_PROCESS is not None:
        return _SERVER_PROCESS
    try:
        with open(process_file(), 'rt') as f:
            text = f.read().strip()
            try:
                pid = int(text)
            except ValueError as e:
                warning(f"Unexpected error parsing {process_file()}:", e, file=sys.stderr)
                return None
        proc = psutil.Process(pid=pid)
        if (actual_name := proc.name()) != "mathicsserver":
            warning(f"WARNING: Unexpected process name {actual_name!r}.\n\tNOTE: cmdline={proc.cmdline()!r}")
        return proc
    except (FileNotFoundError, psutil.NoSuchProcess):
        return None

def shutdown_server(wait=True):
    global _SERVER_PROCESS
    if _SERVER_PROCESS is None:
        return
    if os.name == "posix":
        sig = signal.SIGINT
    elif os.name == "nt":
        sig = signal.CTRL_C_EVENT
    else:
        raise FatalError(f"Unsupported OS: {os.name}")
    _SERVER_PROCESS.send_signal(sig)
    if (code := _SERVER_PROCESS.wait()) != 0:
        warning(f"Server died with code {code}")
    _SERVER_PROCESS = None

def exit():
    shutdown_server()
    

def run_server() -> psutil.Process:
    if (proc := server_process()) is not None:
        return proc
    server_binary = shutil.which("mathicsserver")
    if server_binary is None:       
        raise FatalError("Unable to find `mathicsserver` process")
    Path(local_storage(), "logs").mkdir(exist_ok=True, parents=True)
    child = Popen(
        [server_binary, "--port", str(PORT)],
        stdout=open(Path(local_storage(), "logs/server.log"), "wt"),
        stderr=open(Path(local_storage(), "logs/server.err.log"), "wt"),
    )
    with open(process_file(create=True), 'wt') as f:
        f.write(str(child.pid))
    _SERVER_PROCESS = psutil.Process(pid=child.pid)
    def _server_thread():
        global _SERVER_PROCESS
        return_code = child.wait()
        warning(f"Server died with code {return_code}")
        _SERVER_PROCESS = None
    thread = Thread(target=_server_thread, name="Server Handler")
    thread.daemon = True
    thread.start()


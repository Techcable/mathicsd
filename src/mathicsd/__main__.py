import sys
import multiprocessing as mp
import importlib.resources
import signal

from pystray import Icon, Menu, MenuItem 
import click

from . import FatalError, run_server, PORT, server_process, \
    viewer, warning, local_storage, shutdown_server, load_png_logo
from .viewer import ViewerSettings


WEBVIEW_PROCESSES = []

def spawn_webview(settings, force=False):
    global WEBVIEW_PROCESSES
    if not force and any(proc.is_alive() for proc in WEBVIEW_PROCESSES):
        warning("Webview already exists")
        return
    # We spawn a SUBPROCESS to deal with the webview
    # By spawning a subprocess, we can fix the issues with pystray & webview integration
    # Issues like closing apps & messing with GTK context magically disapear.
    p = mp.Process(target=viewer.spawn_webview, args=(settings,))
    p.start()
    print(f"Spawned webview process: {p.pid}")
    WEBVIEW_PROCESSES.append(p)


def exit(icon):
    shutdown_server()
    for proc in WEBVIEW_PROCESSES:
        proc.terminate()
        proc.wait()
    if icon is not None:
        icon.stop()

def respawn_webview(force=False):
    spawn_webview(ViewerSettings(
        backend=_CURRENT_BACKEND,
        show_startup_msg=False,
        loading_wait=0
    ), force=force)

def handle_user_signal(signum, _frame):
    if signum == signal.SIGUSR1:
        respawn_webview(force=True)

_GUI_MODE = False
_CURRENT_BACKEND = None

@click.command('mathicsd')
@click.option('--backend', default=viewer.detect_default_backend(),
    help="Explicitly specify the webview backend to use.")
@click.option('--hide-startup-msg', is_flag=True,
    help="Suppress the default startup message")
@click.option('--skip-loading-screen', is_flag=True,
    help="Skip the loading screen")
@click.option('--gui', is_flag=True,
    help="Use GUI mode (show dialogs for errors)")
def run(backend, hide_startup_msg, skip_loading_screen, gui):
    global _CURRENT_BACKEND, _GUI_MODE
    if gui:
        _GUI_MODE = True
    _CURRENT_BACKEND = backend
    if (existing_proc := server_process()) is not None:
        print("WARNING: Found existing process. Just spawning a new webview.")
        parent = existing_proc.parent()
        if parent is None:
            raise FatalError("Could not find parent of already-existing server process.....")
        if 'mathicsd' in parent.cmdline():
            parent.send_signal(signal.SIGUSR1)
            return
        else:
            warning("Killing old server")
            existing_proc.terminate()
            existing_proc.wait()
    run_server()
    # TODO: I don't believe SIGUSR1 is portable to Windows...
    signal.signal(signal.SIGUSR1, handle_user_signal)
    spawn_webview(ViewerSettings(
        backend=backend, show_startup_msg=not hide_startup_msg,
        loading_wait=0 if skip_loading_screen else 3
    ))
    icon = Icon(
        "Mathics Daemon", load_png_logo(),
        menu=Menu(
            MenuItem(
                "Open Viewer",
                lambda: respawn_webview()
            ),
            MenuItem(
                "Quit (Stop Server)",
                lambda icon, _: exit(icon)
            )
        )
    )
    try:
        icon.run()
    except KeyboardInterrupt as e:
        # TODO: Broken
        print("Interrupt:", e)
        exit(icon)

def display_gui_error(msg):
    from tkinter import messagebox, Tk
    Tk().withdraw()
    messagebox.showerror("Fatal Error!", msg)

if __name__ == "__main__":
    # We don't want resources (like )
    # TODO: Investigate forkserver?
    mp.set_start_method('spawn')
    try:
        # TODO: How to run click so it doesn't catch KeyboardInterrupt?????
        run.main(standalone_mode=False)
    except FatalError as e:
        display_gui_error(str(e))
        exit(None)
    except KeyboardInterrupt:
        exit(None) # No icon yet

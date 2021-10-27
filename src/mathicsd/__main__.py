import sys
import multiprocessing as mp
import importlib.resources

from pystray import Icon, Menu, MenuItem 
import click

from . import FatalError, run_server, PORT, server_process, \
    viewer, warning, local_storage, shutdown_server, load_png_logo


WEBVIEW_PROCESS = None

_FIRST_RUN=True
def spawn_webview(backend):
    global WEBVIEW_PROCESS
    global _FIRST_RUN
    if WEBVIEW_PROCESS is not None and WEBVIEW_PROCESS.is_alive():
        warning("Webview already exists")
        return
    # We spawn a SUBPROCESS to deal with the webview
    # By spawning a subprocess, we can fix the issues with pystray & webview integration
    # Issues like closing apps & messing with GTK context magically disapear.
    p = mp.Process(target=viewer.spawn_webview, args=(backend, _FIRST_RUN))
    _FIRST_RUN=False
    p.start()
    print(f"Spawned webview process: {p.pid}")
    WEBVIEW_PROCESS = p


def exit(icon):
    shutdown_server()
    WEBVIEW_PROCESS.terminate()
    icon.stop()

@click.command('mathicsd')
@click.option('--backend', default=viewer.detect_default_backend(),
    help="Explicitly specify the webview backend to use.")
def run(backend='qt'):
    run_server()
    spawn_webview(backend)
    icon = Icon(
        "Mathics Daemon", load_png_logo(),
        menu=Menu(
            MenuItem(
                "Open Viewer",
                lambda: spawn_webview(backend)
            ),
            MenuItem(
                "Quit (Stop Server)",
                lambda icon, _: exit(icon)
            )
        )
    )
    try:
        icon.run()
    except (KeyboardInterrupt, click.Abort) as e:
        # TODO: Broken
        print("Interrupt:", e)
        exit(icon)

if __name__ == "__main__":
    # We don't want resources (like )
    # TODO: Investigate forkserver?
    mp.set_start_method('spawn')
    # TODO: How to run click so it doesn't catch KeyboardInterrupt?????
    run()

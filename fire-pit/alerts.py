"""Lightweight alerts using GTK3 (or fallback to console if installed)"""
import sys

try:
    import gi
    gi.require_version("Gtk", "3.0")   
    from gi.repository import Gtk
    BACKEND='GTK'
except ImportError:
    print("WARN: GTK bindings not found. Falling back to console", file=sys.stderr)
    BACKEND=None

def gtk_alert(msg: str) -> AssertionError:
    if BACKEND == "GTK":
        window = Gtk.MessageDialog(title="ERROR!!", type=Gtk.MessageType.ERROR)
        window.set_markup("Fatal Error: " + msg)
        window.show()
        window.connect("destroy", Gtk.main_quit)
        Gtk.main()
        sys.exit(1)
    elif BACKEND is None:
        print("Fatal error:", msg, file=sys.stderr)
        sys.exit(1)
    else:
        raise AssertionError("Unknown backend: " + BACKEND)
    raise AssertionError # unreachable
mathicsd
==========
A convenient dameon to manage [mathics-django](https://github.com/Mathics3/mathics-django) instances.

It ensures that only a single instance of the server
is running at a time, and shows a small icon in the system status bar
(similar to discord).

## Requirements
- [pystray](https://github.com/moses-palmer/pystray)
- [Mathics](https://mathics.org) and [`mathics-django`](https://github.com/Mathics3/mathics-django)
- A web browser (preferbly Firefox)


## Browser Integration
Since 'mathics-django' is a web-application, it needs a web browser to use it.

The icon in the status bar contains three options:

1. Spawn a a dedicated window (*NOTE: Requires Firefox*)
   - Once this is done, you can click on the status icon to bring that window into focus.
   - Exiting the dedicated window simply kills the browser, not the underlying server.
2. Spawn a new tab (in an existing window)
   - Works with any browser supported by the [`webbrowser`](https://docs.python.org/3/library/webbrowser.html) module
    - `mathicsd` cannot keep track of the tab, so unlike with the dedicated window clicking on the icon can't bring it back into focus after it's been spawned.
    - It also cannot "reuse" any existing tabs
3. Spawn a new window
    - NOTE: This window is *not dedicated*, so it differs 
    - This is very similar to option 2. It uses the same `webbrowser` module and also cannot keep track of the window

If Firefox is present, 1 is the default, otherwise 2 is.


## Memory Uage
NOTE: This is moderately memory intensive, so if your system is memory constrained (mine is) I wouldn't recommend enabling this at startup.

By my informal tests, the server initially requires 244MB of memory. Even max . Because Firefox and other web browsers are often able to reuse memory between instances, the memory usage of the client is much more complex. By my tests, starting up a blank firefox instance takes almost 1G of memory (but this is true). Most likely you will have another firefox instance already open. If you open in a new tab, the additional window takes about 164MB of RAM. If you open in a new window, that can be  more expensive and take like 200+MB of RAM.

So essentially, the server takes between 244MB and 270MB of RAM. Assuming you have other firefox windows open, adding a dedicated window should take no more than 200-300 MB of RAM.

TLDR; 300MB for just the plain server, 400 MB for server + tab, and 600 MB for server + dedicated window.

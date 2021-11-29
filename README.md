mathicsd
==========
A convenient webview frontend to [Mathics](https://mathics.org/).

Uses [mathics-django](https://github.com/Mathics3/mathics-django) as the underlying server.

It ensures that only a single instance of the server
is running at a time, and shows a small icon in the system status bar
(similar to discord).

## Requirements
- [pywebview](https://github.com/r0x0r/pywebview)
- [pystray](https://github.com/moses-palmer/pystray)
- [psutil](https://github.com/giampaolo/psutil)
- [Mathics](https://mathics.org) and [`mathics-django`](https://github.com/Mathics3/mathics-django)
   - NOTE: `mathicsserver` command must be in `$PATH` and directly runnable. 

## Install
`pip install --user mathicsd`

On linux, run `./install/install_desktop.py` to create the desktop file.

TODO: Better installation (ie. run 'install_desktop.py' automatically and make cross-platform).

## Licensing
[Mathics](https://mathics.org/) is free-software, licensed under the GPLv3 ([Wikipedia page](https://en.wikipedia.org/wiki/GNU_General_Public_License)).

`mathicsd` is a third-party project. It is also licensed under the GPLv3. See [the license file](./LICENSE.md) for more details).

## Memory usage
The `mathicsd` process itself requires like 12MB. That's like a 5-10% overhead (not much.) 

The `mathicsserver` requires 432 MB. The bulk of the 

With '--backend gtk', it spawns two `WebKit` subprocesses which requires around 240 MB
With '--backend qt' it spawns two chromium subprocess which require about 196MB

This is a little strange, since Chromium has a worse reputation for memory usage :shrug:

Anyways, the web frontend is going to take half the memory of the server. It can be closed at any time....

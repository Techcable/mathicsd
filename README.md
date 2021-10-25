mathicsd
==========
A convenient daemon to manage [mathics-django](https://github.com/Mathics3/mathics-django) instances.

It ensures that only a single instance of the server
is running at a time, and shows a small icon in the system status bar
(similar to discord).

## Requirements
- [pywebview](https://github.com/r0x0r/pywebview)
- [pystray](https://github.com/moses-palmer/pystray)
- [psutil](https://github.com/giampaolo/psutil)
- [Mathics](https://mathics.org) and [`mathics-django`](https://github.com/Mathics3/mathics-django)
   - NOTE: `mathicsserver` command must be in `$PATH` and directly runnable. 

## Memory usage
The `mathicsd` process itself requires like 12MB (not much)

The `mathicsserver` requires 432 MB 

With '--backend gtk', it spawns two `WebKit` subprocesses which requires around 240 MB
With '--backend qt' it spawns two chromium subprocess which require about 196MB

This is a little strange, since Chromium has a worse reputation for memory usage :P

Anyways, the web frontend is going to take half the memory of, and can be closed whenever....

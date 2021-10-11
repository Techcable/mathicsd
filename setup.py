from setuptools import setup

setup(
    name="mathicsd",
    version="0.1.0",
    install_requires=[
        # Used for system tray icon 
        "pystray",
        # We require mathics (obviously)
        "Mathics3",
        # We also require mathics-django (for our server)
        "mathics-django",
    ]
)

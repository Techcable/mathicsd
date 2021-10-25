from setuptools import setup, find_packages

setup(
    name="mathicsd",
    version="0.1.0",
    install_requires=[
        "pywebview",
        # Used for system tray icon 
        "pystray",
        # We require mathics (obviously)
        "Mathics3",
        # Used to check whether or not we actually have a connection
        "requests",
        # Used for CLI
        "click",
        # Used for tray icons
        "Pillow",
        # We also require mathics-django (for our server)
        "mathics-django",
    ],
    packages=find_packages(
        where='src',
        include=['pkg*'],
        exclude=['additional'],
    ),
    package_dir={"": "src"},
    include_package_data=True
)

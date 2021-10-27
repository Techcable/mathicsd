#!/usr/bin/env python3
import os
import sys

from pathlib import Path

DESKTOP_FILE = "mathicsd.desktop"

if os.name != "posix" or sys.platform == "darwin":
    print(f"Cannot use Linux .desktop files on {sys.platform}", file=sys.stderr)
    sys.exit(1)

try:
    import mathicsd
    install_location = Path(mathicsd.__file__)
except ImportError as e:
    print(f"Unable to import `mathicsd` (to determine location): {e}", file=sys.stderr)
    print("Has it been installed yet??", file=sys.stderr)
    sys.exit(1)
    
if not install_location.is_file():
    print(f"ERROR: mathicsd.__file__ ({install_location}) doesn't actually exist", file=sys.stderr)
    sys.exit(1)

# TODO: Can we use SVG logos?
logo_file = Path(install_location.parent, "resources/logo.png")
assert logo_file.exists(), "Missing logo file"

this_file = Path(__file__)
if not this_file.exists():
    print(f"Unable to detect {self.file} (got {__file__!r}", file=sys.stderr)
    sys.exit(1)

desktop_template = Path(this_file.parent, DESKTOP_FILE)
desktop_applications_dir = Path(Path.home(), ".local/share/applications")

with open(desktop_template) as f:
    template_text = f.read()

assert template_text.strip(), "Empty template"

actual_desktop_file = template_text.replace("{{ICON_LOCATION}}", str(logo_file)) 
assert actual_desktop_file.strip(), "Empty result"
target_location = Path(desktop_applications_dir, DESKTOP_FILE)
print(f"Installing {DESKTOP_FILE} to {target_location}")
if target_location.exists():
    print("  WARNING: Overriding existing file")

with open(target_location, 'wt') as f:
    f.write(actual_desktop_file)

import stat
print(f"Marking {target_location} executable...")
target_location.chmod(target_location.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

assert target_location.exists()
print("DONE!")



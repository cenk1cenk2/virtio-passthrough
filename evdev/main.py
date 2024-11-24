#!/usr/bin/env python3

import evdev
import re
import collections

devices = {}

ignores = [
    "^HD-Audio.*$",
    "^HDA.*$",
    "^Power Button.*$",
    "^PC Speaker.*$",
    "^.*Control$",
]

for path in evdev.list_devices():
    try:
        device = evdev.InputDevice(path)

        if any([re.search(ignore, device.name) for ignore in ignores]):
            print(f"Ignoring by expression: {device.name}")
            continue

        if device.name not in devices:
            devices[device.name] = []

        devices[device.name].append({"device": device, "path": path})
    except:  # noqa: E722
        print(f"Failed to open {path}")

print()
print("evdev-proxy devices")
print()
for name, device in collections.OrderedDict(devices.items()).items():
    c = ""
    if name.endswith("Mouse"):
        c = "Mouse"
    elif name.endswith("Keyboard"):
        c = "Keyboard"
    print()
    print(f"# {name}")
    print("[[device.Simple.selector]]")
    print(
        f"USBIDClass = {{ vendor = 0x{device[0]['device'].info.vendor:04x}, model = 0x{device[0]['device'].info.product:04x}, class = '{c}' }}"
    )

#!/usr/bin/env python3

from os import walk
import evdev

devices = {}

for _, _, filenames in walk("/dev/input/by-id"):
    for file in sorted(filenames):
        try:
            path = f"/dev/input/by-id/{file}"
            device = evdev.InputDevice(path)

            if device.name not in devices:
                devices[device.name] = []

            devices[device.name].append({"device": device, "path": path})
        except:  # noqa: E722
            pass

for name, device in devices.items():
    print(f"[DEVICE] {name}")
    for subdevice in device:
        print(f"[PATH] {subdevice['path']}")

    print()

print("Almost done!")

print()
print("evdev inputs")
print()

for name, device in devices.items():
    print("<input type='evdev'>")
    print(f"  <source dev='{device[0]['path']}' grab='all' repeat='on'/>")
    print("</input>")

print()
print("evdev devices")
print()
for name, device in devices.items():
    print("[[device.Simple.selector]]")
    print(f"# {name}")
    print(
        f"USBIDClass = {{ vendor = 0x{device[0]['device'].info.vendor:04x}, model = 0x{device[0]['device'].info.product:04x}, class = '' }}"
    )

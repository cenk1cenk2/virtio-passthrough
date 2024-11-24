#!/usr/bin/env python3

import evdev
import re
from itertools import groupby
import sys
import argparse

parser = argparse.ArgumentParser(description="Generate evdev-proxy configuration")
parser.add_argument("subcommand", choices=["evdev-proxy", "udev"], help="subcommand")
args = parser.parse_args()

ignores = [
    "^HD-Audio.*$",
    "^HDA.*$",
    "^Power Button.*$",
    "^PC Speaker.*$",
]

all_devices = []
for path in evdev.list_devices():
    try:
        device = evdev.InputDevice(path)

        if any([re.search(ignore, device.name) for ignore in ignores]):
            print(f"Ignoring by expression: {device.name}", file=sys.stderr)

            continue

        all_devices.append(device)

    except:  # noqa: E722
        print(f"Failed to open {path}", file=sys.stderr)

devices = groupby(
    sorted(all_devices, key=lambda x: x.name),
    lambda x: x.name and x.info.vendor and x.info.product,
)

if args.subcommand == "evdev-proxy":
    conf = []

    for _, subdevices in devices:
        device = next(subdevices)

        conf.append("")
        conf.append(f"# {device.name}")
        conf.append("[[device.Simple.selector]]")
        conf.append(
            f"USBIDClass = {{ vendor = 0x{device.info.vendor:04x}, model = 0x{device.info.product:04x}, class = 'Mouse' }}"
        )
        conf.append("[[device.Simple.selector]]")
        conf.append(
            f"USBIDClass = {{ vendor = 0x{device.info.vendor:04x}, model = 0x{device.info.product:04x}, class = 'Keyboard' }}"
        )

        print(f"Generated configuration for device: {device.name}", file=sys.stderr)

    print("evdev-proxy file will be generated.", file=sys.stderr)
    print("-------------------------------------", file=sys.stderr)
    print("\n".join(conf))

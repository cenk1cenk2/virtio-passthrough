#!/usr/bin/env python3

import evdev
import re
from itertools import groupby
import sys

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

conf = [
    """
log_level = "INFO"

##### Devices #####
# !!! IMPORTANT NOTE !!!
# Virtual device name should start with 'EvdevProxy' prefix, otherwise default
# udev rules from '70-uinput-evdev-proxy.rules' won't create device symlink in
# '/dev/input/by-id/' directory. If you want to use another name make sure to
# configure udev accordingly.
#
# Available device types:
#  * Simple -- Single virtual device that capture and proxy all devices that
#              match any of it's selectors
#    Parameters:
#      * vendor (int)     -- 16-bit device vendor ID
#      * model (int)      -- 16-bit model vendor ID
#      * class (enum)     -- device class (Mouse/Keyboard/AIO),
#                            AIO - all-in-one, device that acts both as KB
#                            and Mouse
#      * selector (array) -- list of selectors that specify criteria used to
#                            select witch real evdev devices this virtual
#                            device should proxy
#
#    Available device selectors:
#      * USBID      -- Simple selector that blindly selects usb device based
#                      on it's usb vendor:model identificator
#      * USBIDClass -- Simple selector that blindly selects usb device based
#                      on it's usb vendor:model identificator and device
#                      class (Mouse/Keyboard), useful for wireless devices
#                      with single receiver (e.g. Logitech Unifying Receiver)
#

[[device]]
[device.Simple]
name = "EvdevProxyAIO"
vendor = 0x1337
model = 0x1337
class = "AIO"
""",
]

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

print("Configuration file will be generated.", file=sys.stderr)
print("-------------------------------------", file=sys.stderr)
print("\n".join(conf))

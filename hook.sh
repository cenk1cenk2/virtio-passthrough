#!/bin/bash

set -e

DATE=$(date +"%Y-%m-%dZ%R:%S")

function replace() {
  local file="$1"
  local resource="$2"
  if test -e "$file"; then
    rm "$file"
  fi

  cp "$resource" "$file"

  echo "[$DATE] $file installed."
}

mkdir -p /etc/libvirt/hooks

replace "/etc/libvirt/hooks/qemu" "hooks/qemu"
replace "/usr/local/bin/vfio-startup" "hooks/vfio-startup"
replace "/usr/local/bin/vfio-teardown" "hooks/vfio-teardown"

replace "/etc/systemd/system/libvirt-nosleep@.service" "systemd/libvirt-nosleep@.service"
replace "/etc/systemd/system/evdev-proxy.service" "systemd/evdev-proxy.service"
systemctl daemon-reload

replace "/etc/evdev-proxy/config.toml" "evdev-proxy/config.toml"

echo "Hooks are installed."

#!/bin/bash

if test -e /etc/libvirt/ && ! test -e /etc/libvirt/hooks; then
  mkdir -p /etc/libvirt/hooks
fi
if test -e /etc/libvirt/hooks/qemu; then
  mv /etc/libvirt/hooks/qemu /etc/libvirt/hooks/qemu.bak
fi
if test -e /usr/local/bin/vfio-startup; then
  mv /usr/local/bin/vfio-startup /usr/local/bin/vfio-startup.bak
fi
if test -e /usr/local/bin/vfio-teardown; then
  mv /usr/local/bin/vfio-teardown /usr/local/bin/vfio-teardown.bak
fi
if test -e /etc/systemd/system/libvirt-nosleep@.service; then
  rm /etc/systemd/system/libvirt-nosleep@.service
fi
if test -e /etc/evdev-proxy/config.toml; then
  mv /etc/evdev-proxy/config.toml /etc/evdev-proxy/config.toml.bak
fi

cp systemd-no-sleep/libvirt-nosleep@.service /etc/systemd/system/libvirt-nosleep@.service
cp hooks/vfio-startup /usr/local/bin/vfio-startup
cp hooks/vfio-teardown /usr/local/bin/vfio-teardown
cp hooks/qemu /etc/libvirt/hooks/qemu
cp evdev-proxy/config.toml /etc/evdev-proxy/config.toml

chmod +x /usr/local/bin/vfio-startup
chmod +x /usr/local/bin/vfio-teardown
chmod +x /etc/libvirt/hooks/qemu
chmod +x /etc/evdev-proxy/config.toml

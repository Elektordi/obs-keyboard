#!/bin/sh

cp 90-extra-keyboard.hwdb /etc/udev/hwdb.d/90-extra-keyboard.hwdb
systemd-hwdb update
udevadm trigger


#!/usr/bin/env bash
# Run ONCE on each lab PC (the host, not inside the container):
#   sudo bash scripts/install_udev_rules.sh
# Gives the SO-100 servo board a stable name (/dev/so100) and lets every user open it.
# The Waveshare/Feetech boards use a WCH USB-serial chip (CH340 1a86:7523 or CH343 1a86:55d3).
set -e
RULE=/etc/udev/rules.d/99-so100.rules
cat > "$RULE" <<'RULES'
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", SYMLINK+="so100", MODE="0666"
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="55d3", SYMLINK+="so100", MODE="0666"
RULES
udevadm control --reload-rules && udevadm trigger
echo "Installed $RULE. Unplug and replug the robot, then check: ls -l /dev/so100"
echo "Not found? Run 'lsusb' and add your board's vendor:product IDs to $RULE."

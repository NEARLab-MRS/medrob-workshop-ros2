#!/usr/bin/env bash
# Lab 0 self-check: confirms ROS 2, the workspace and the desktop are working.
ok()   { echo "  [OK]   $1"; }
fail() { echo "  [FAIL] $1"; FAILED=1; }
FAILED=0

echo "Checking your ROS 2 lab environment..."

[ "$ROS_DISTRO" = "jazzy" ] && ok "ROS 2 Jazzy is sourced" \
  || fail "ROS 2 not sourced. Open a new terminal or run: source /opt/ros/jazzy/setup.bash"

command -v ros2 >/dev/null && ok "ros2 command available" || fail "ros2 command not found"

ros2 pkg list 2>/dev/null | grep -q '^lab_starter$' && ok "lab_starter package is built" \
  || fail "lab_starter not found. Run: cb   (or: colcon build && source install/setup.bash)"

[ -n "$DISPLAY" ] && ok "DISPLAY is set to $DISPLAY" || fail "DISPLAY is not set"

if command -v curl >/dev/null && curl -s -o /dev/null http://localhost:6080; then
  ok "Desktop (noVNC) is running on port 6080"
else
  fail "Desktop not reachable on port 6080. Check the PORTS tab."
fi

echo
if [ "$FAILED" = 0 ]; then
  echo "All good! Open the PORTS tab, click the globe next to port 6080, and log in with password: vscode"
else
  echo "Some checks failed. Ask your instructor or see README.md > Troubleshooting."
fi

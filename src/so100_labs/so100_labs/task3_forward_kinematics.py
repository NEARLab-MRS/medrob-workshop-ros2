"""Task 3 - Forward kinematics.

Goal: compute where the tool centre point (TCP) is, given the 5 joint angles,
using homogeneous transforms built from the URDF (robot_model.CHAIN).

Run (simulation, terminal 1):
    ros2 launch so100_bringup arm.launch.py
Run your code (terminal 2) - it compares your FK with TF from robot_state_publisher:
    ros2 run so100_labs task3_forward_kinematics
Test:
    pytest src/so100_labs/test/test_task3_forward_kinematics.py

URDF conventions (this is exactly what robot_state_publisher does):
  * For each joint: T = T @ Trans(xyz) @ Rot(rpy) @ Rot(axis, q)
  * Rot(rpy) = Rz(yaw) @ Ry(pitch) @ Rx(roll)      (fixed-axis roll, pitch, yaw)
  * Rot(axis, q): rotation by angle q about the unit vector `axis` (Rodrigues' formula)
  * After the last joint: T = T @ Trans(TCP_XYZ)
"""
import math

import numpy as np

from so100_labs.arm import run
from so100_labs.robot_model import APPROACH_AXIS, CHAIN, POSES, TCP_XYZ  # noqa: F401


def rotation_from_rpy(roll, pitch, yaw):
    """3x3 rotation matrix Rz(yaw) @ Ry(pitch) @ Rx(roll)."""
    # TODO(student): implement
    raise NotImplementedError('Task 3: rotation_from_rpy')


def rotation_about_axis(axis, angle):
    """3x3 rotation of `angle` rad about `axis` (normalise it first). Rodrigues' formula:
    R = I + sin(a) K + (1 - cos(a)) K^2, with K the skew-symmetric matrix of the axis."""
    # TODO(student): implement
    raise NotImplementedError('Task 3: rotation_about_axis')


def homogeneous(rotation, translation):
    """4x4 homogeneous transform from a 3x3 rotation and a 3-vector translation."""
    # TODO(student): implement
    raise NotImplementedError('Task 3: homogeneous')


def forward_kinematics(q):
    """4x4 pose of tcp_link in base_link for joint vector q (5 values, ARM_JOINTS order)."""
    # TODO(student): implement using CHAIN and TCP_XYZ
    raise NotImplementedError('Task 3: forward_kinematics')


# ---- Provided helpers built on your forward_kinematics -----------------------------
def tcp_position(q):
    """TCP position [x, y, z] in base_link."""
    return forward_kinematics(q)[:3, 3]


def approach_pitch(q):
    """Angle [rad] of the gripper's approach direction below the horizontal plane.
    pi/2 = pointing straight down, 0 = horizontal."""
    a = forward_kinematics(q)[:3, :3] @ np.asarray(APPROACH_AXIS)
    return math.atan2(-a[2], math.hypot(a[0], a[1]))


def main_sequence(arm):
    """Provided: move through poses and compare your FK with TF."""
    worst = 0.0
    for name in ['home', 'ready', 'left', 'right']:
        arm.move_to(POSES[name])
        arm.sleep(0.5)
        q = arm.joint_positions()
        mine, tf = tcp_position(q), arm.tcp_position()
        error = float(np.linalg.norm(mine - tf))
        worst = max(worst, error)
        arm.get_logger().info(f'{name:6s} FK={np.round(mine, 4)} TF={np.round(tf, 4)} '
                              f'error={error * 1000:.2f} mm')
    arm.move_to(POSES['home'])
    return worst < 0.001


def main():
    run(main_sequence)


if __name__ == '__main__':
    main()

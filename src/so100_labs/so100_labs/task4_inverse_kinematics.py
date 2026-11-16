"""Task 4 - End-effector commands with inverse kinematics (IK).

Goal: command the arm in Cartesian space: "put the gripper at (x, y, z) with this
approach pitch". The SO-100 has only 5 joints, so an arbitrary 6-D pose (position +
full orientation) is NOT reachable. We control 4 things with the first 4 joints:
    task vector f(q) = [x, y, z, pitch]
and keep wrist_roll at whatever value the seed has.

Method - damped least squares (Levenberg-Marquardt):
    repeat:
        e   = target - f(q)
        J   = d f / d q[0:4]          (4x4, by finite differences)
        dq  = J^T (J J^T + lambda^2 I)^-1 e
        q[0:4] += dq, then clamp q[0:4] into the joint limits
    until |e_position| < tol (and |e_pitch| < 10*tol), else raise UnreachableError

Run (simulation, terminal 1):  ros2 launch so100_bringup arm.launch.py
Run your code (terminal 2):    ros2 run so100_labs task4_inverse_kinematics
Test:  pytest src/so100_labs/test/test_task4_inverse_kinematics.py
Requires Task 3 (forward kinematics).
"""
import math

import numpy as np

from so100_labs.arm import run
from so100_labs.robot_model import LOWER, POSES, UPPER  # noqa: F401
from so100_labs.task3_forward_kinematics import approach_pitch, tcp_position


class UnreachableError(ValueError):
    pass


def task_vector(q):
    """Provided: [x, y, z, pitch] of the TCP for joint vector q."""
    return np.array([*tcp_position(q), approach_pitch(q)])


def numerical_jacobian(q, eps=1e-6):
    """4x4 Jacobian of task_vector with respect to the first 4 joints (forward differences)."""
    # TODO(student): implement
    raise NotImplementedError('Task 4: numerical_jacobian')


def inverse_kinematics(target_xyz, pitch, q_seed, tol=1e-4, max_iterations=200, damping=0.01):
    """Joint vector (list of 5) that puts the TCP at target_xyz with the given pitch.

    Start from q_seed (5 values; q_seed[4] = wrist roll is kept unchanged).
    Tip: weight the pitch row lower than the position rows (e.g. 0.1), since 1 rad of
    pitch is a much bigger number than a few centimetres of position.
    Raise UnreachableError if it does not converge within max_iterations.
    """
    # TODO(student): implement
    raise NotImplementedError('Task 4: inverse_kinematics')


TARGETS = [
    # x, y, z [m] in base_link, pitch [rad]
    ((0.0, -0.25, 0.10), math.radians(60)),
    ((0.10, -0.22, 0.05), math.radians(90)),
    ((-0.10, -0.22, 0.05), math.radians(90)),
    ((0.0, -0.30, 0.15), math.radians(30)),
]


def main_sequence(arm):
    """Provided: visit each Cartesian target and report the error measured with TF."""
    q = arm.joint_positions()
    arm.show_points([t for t, _ in TARGETS])
    for xyz, pitch in TARGETS:
        try:
            q = inverse_kinematics(xyz, pitch, q)
        except UnreachableError as e:
            arm.get_logger().error(str(e))
            return False
        if not arm.move_to(q):
            return False
        arm.sleep(0.3)
        err = np.linalg.norm(arm.tcp_position() - np.array(xyz))
        arm.get_logger().info(f'target {xyz}: reached with error {err * 1000:.1f} mm')
    return arm.move_to(POSES['home'])


def main():
    run(main_sequence)


if __name__ == '__main__':
    main()

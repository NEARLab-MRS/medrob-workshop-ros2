"""Task 5 - Cartesian paths: draw a square, then pick and place.

Goal: move the TCP along STRAIGHT LINES in Cartesian space (not joint space) by
running IK on many closely spaced points, and combine this with the gripper.

Run (Gazebo has a table and a cube; terminal 1):
    ros2 launch so100_bringup arm.launch.py backend:=gazebo
Run your code (terminal 2):
    ros2 run so100_labs task5_cartesian
Test:  pytest src/so100_labs/test/test_task5_cartesian.py
Requires Tasks 3 and 4.
"""
import math

import numpy as np  # noqa: F401

from so100_labs.arm import run
from so100_labs.robot_model import GRIPPER_CLOSED, GRIPPER_OPEN, MAX_VELOCITY, POSES  # noqa: F401
from so100_labs.task4_inverse_kinematics import inverse_kinematics

DOWN = math.radians(90)  # gripper pointing straight down


def linear_interpolation(p0, p1, step=0.005):
    """Points on the straight segment p0 -> p1, INCLUDING both ends, spaced at most `step` m
    apart and evenly spaced. Return a list of [x, y, z] lists."""
    # TODO(student): implement
    raise NotImplementedError('Task 5: linear_interpolation')


def square_corners(center, side):
    """Provided: 5 corners of a horizontal square (the first corner is repeated at the end)."""
    cx, cy, cz = center
    h = side / 2
    return [(cx - h, cy - h, cz), (cx + h, cy - h, cz), (cx + h, cy + h, cz),
            (cx - h, cy + h, cz), (cx - h, cy - h, cz)]


def cartesian_path(points, pitch, q_seed):
    """Joint vectors for every Cartesian point (same pitch for all).
    Seed each IK call with the previous solution so the arm moves continuously."""
    # TODO(student): implement
    raise NotImplementedError('Task 5: cartesian_path')


def time_parametrize(joint_path, q_start, max_velocity=MAX_VELOCITY * 0.5, min_dt=0.05):
    """Times (seconds from start) to reach each joint vector of joint_path, starting from q_start.
    Each step lasts max(min_dt, largest joint change / max_velocity)."""
    # TODO(student): implement
    raise NotImplementedError('Task 5: time_parametrize')


def follow_cartesian(arm, points, pitch):
    """Provided: move the TCP through `points` along the straight lines between them."""
    q0 = arm.joint_positions()
    path = cartesian_path(points, pitch, q0)
    return arm.follow_trajectory(time_parametrize(path, q0), path)


def draw_square(arm, center=(0.0, -0.24, 0.05), side=0.08):
    """Provided: draw a square with the TCP pointing down."""
    corners = square_corners(center, side)
    arm.show_points(corners, ns='square')
    if not arm.move_to(inverse_kinematics(corners[0], DOWN, arm.joint_positions())):
        return False
    points = []
    for a, b in zip(corners[:-1], corners[1:]):
        points += linear_interpolation(a, b)[1:]
    return follow_cartesian(arm, points, DOWN)


def pick_and_place(arm, pick=(0.08, -0.22, 0.013), place=(-0.08, -0.22, 0.013), hover=0.06):
    """Pick an object at `pick` and put it down at `place`.

    TODO(student): implement this sequence. Every step must succeed (return True):
      1. open the gripper                         arm.gripper(GRIPPER_OPEN)
      2. move (joint space) above the pick point  arm.move_to(inverse_kinematics(...))
      3. straight line down to the pick point     follow_cartesian(arm, linear_interpolation(...), DOWN)
      4. close the gripper
      5. straight line up, then over to above the place point, then down
      6. open the gripper
      7. straight line back up
    "Above" means `hover` metres higher in z. Return True if everything succeeded.
    """
    arm.show_points([pick, place], ns='pick_place', color=(0.9, 0.2, 0.2))
    raise NotImplementedError('Task 5: pick_and_place')


def main_sequence(arm):
    ok = draw_square(arm) and pick_and_place(arm)
    return ok and arm.move_to(POSES['home'])


def main():
    run(main_sequence)


if __name__ == '__main__':
    main()

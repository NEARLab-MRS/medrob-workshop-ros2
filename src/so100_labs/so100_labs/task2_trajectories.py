"""Task 2 - Joint trajectories.

Goal: generate a smooth, time-parametrised trajectory through several poses and
let `joint_trajectory_controller` execute it (FollowJointTrajectory action).

Run (simulation, terminal 1):
    ros2 launch so100_bringup arm.launch.py
Run your code (terminal 2):
    ros2 run so100_labs task2_trajectories
Test:
    pytest src/so100_labs/test/test_task2_trajectories.py

Background - quintic (5th order) blend with zero velocity and acceleration at both ends:
    s = t / T                       (0 <= s <= 1)
    b(s) = 10 s^3 - 15 s^4 + 6 s^5
    q(t) = q0 + (q1 - q0) * b(s)
    q'(t) = (q1 - q0) * b'(s) / T,   b'(s) = 30 s^2 - 60 s^3 + 30 s^4
The peak of b'(s) is 15/8 (at s = 0.5).
"""
import math  # noqa: F401

import numpy as np  # noqa: F401

from so100_labs.arm import run
from so100_labs.robot_model import MAX_VELOCITY, POSES

PEAK_VELOCITY_FACTOR = 15.0 / 8.0


def quintic(q0, q1, duration, t):
    """Position and velocity of the quintic blend from q0 to q1 at time t.

    q0, q1: joint vectors (lists or arrays). Returns (position, velocity) as numpy arrays.
    For t < 0 or t > duration, clamp t into [0, duration].
    """
    # TODO(student): implement
    raise NotImplementedError('Task 2: quintic')


def minimum_duration(q0, q1, max_velocity=MAX_VELOCITY):
    """Shortest duration T so that no joint exceeds max_velocity during quintic(q0, q1, T, .).

    Hint: the joint that moves the furthest is the limiting one.
    """
    # TODO(student): implement
    raise NotImplementedError('Task 2: minimum_duration')


def sample_trajectory(waypoints, max_velocity=MAX_VELOCITY, dt=0.1):
    """Chain quintic segments between consecutive waypoints and sample them every dt seconds.

    Returns (times, positions, velocities):
      times      : increasing list of seconds from the start, first element = dt
      positions  : list of joint vectors (lists), one per time
      velocities : list of joint velocity vectors (lists), one per time
    Each segment lasts minimum_duration(...) rounded UP to a multiple of dt (at least dt),
    and the robot stops (zero velocity) at every waypoint. The last sample is exactly the
    last waypoint.
    """
    # TODO(student): implement
    raise NotImplementedError('Task 2: sample_trajectory')


def main_sequence(arm):
    """Provided: plan through several poses and execute in one trajectory."""
    names = ['home', 'ready', 'left', 'right', 'ready', 'home']
    waypoints = [arm.joint_positions()] + [POSES[n] for n in names]
    times, positions, velocities = sample_trajectory(waypoints)
    arm.get_logger().info(f'Sending {len(times)} points, {times[-1]:.1f} s')
    return arm.follow_trajectory(times, positions, velocities)


def main():
    run(main_sequence)


if __name__ == '__main__':
    main()

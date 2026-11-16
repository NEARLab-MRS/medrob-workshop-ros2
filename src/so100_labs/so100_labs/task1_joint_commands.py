"""Task 1 - Joint-space commands.

Goal: drive the arm through a sequence of named poses by sending joint positions
directly to `forward_position_controller`.

Run (simulation, terminal 1):
    ros2 launch so100_bringup arm.launch.py controller:=position
Run your code (terminal 2):
    ros2 run so100_labs task1_joint_commands
Test:
    pytest src/so100_labs/test/test_task1_joint_commands.py

forward_position_controller applies every command immediately, so a big jump
would make the arm snap to the target. That is why you send many small steps
(`interpolate_steps`) at RATE_HZ. In Task 2 you will let a trajectory controller
do this for you.
"""
import math  # noqa: F401  (you will probably need it)

from so100_labs.arm import run
from so100_labs.robot_model import ARM_JOINTS, LOWER, POSES, UPPER  # noqa: F401

RATE_HZ = 50.0
MAX_STEP = 0.02  # rad per command -> at most 1 rad/s at 50 Hz


def order_joints(named_positions):
    """Convert {joint_name: position} into a list ordered like ARM_JOINTS.

    Example: {'wrist_roll_joint': 1.0, 'shoulder_pan_joint': 0.5, ...}
             -> [0.5, ..., 1.0]
    Values must be floats. If a joint is missing, raise KeyError.
    """
    # TODO(student): implement
    raise NotImplementedError('Task 1: order_joints')


def clamp_to_limits(q):
    """Return a copy of `q` where every joint is clamped into [LOWER[i], UPPER[i]]."""
    # TODO(student): implement
    raise NotImplementedError('Task 1: clamp_to_limits')


def interpolate_steps(q_start, q_goal, max_step=MAX_STEP):
    """Split the motion q_start -> q_goal into small, evenly spaced steps.

    Return a list of joint vectors. Rules:
      * no joint may change by more than `max_step` between consecutive vectors
        (the first vector is compared to q_start),
      * use as few steps as possible (n = ceil(largest joint change / max_step), at least 1),
      * all joints move simultaneously (linear interpolation),
      * the last vector equals q_goal; q_start itself is NOT included.
    """
    # TODO(student): implement
    raise NotImplementedError('Task 1: interpolate_steps')


def main_sequence(arm):
    """Visit home -> ready -> left -> right -> home. (Provided - read it!)"""
    sequence = ['home', 'ready', 'left', 'right', 'home']
    q = arm.joint_positions()
    for name in sequence:
        goal = clamp_to_limits(POSES[name])
        arm.get_logger().info(f'Moving to {name}: {goal}')
        for step in interpolate_steps(q, goal):
            arm.send_joint_positions(step)
            arm.sleep(1.0 / RATE_HZ)
        arm.sleep(0.5)
        q = goal
    return True


def main():
    run(main_sequence)


if __name__ == '__main__':
    main()

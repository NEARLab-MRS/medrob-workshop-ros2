# SO-100 arm labs

Five tasks that build on each other, from raw joint commands to Cartesian pick-and-place. You write
code in `src/so100_labs/so100_labs/taskN_*.py`, wherever you see `TODO(student)`.

| #   | Task                               | You learn                                                | Guide                          |
| --- | ---------------------------------- | -------------------------------------------------------- | ------------------------------ |
| 1   | Joint-space commands               | topics, joint order, limits, why step commands are jerky | [01](01_joint_commands.md)     |
| 2   | Joint trajectories                 | actions, time parametrisation, quintic polynomials       | [02](02_trajectories.md)       |
| 3   | Forward kinematics                 | homogeneous transforms, URDF, TF                         | [03](03_forward_kinematics.md) |
| 4   | Inverse kinematics                 | Jacobian, damped least squares, reachability             | [04](04_inverse_kinematics.md) |
| 5   | Cartesian paths and pick-and-place | straight-line motion, gripper, task sequencing           | [05](05_cartesian.md)          |
| ★   | Bonus: MoveIt                      | position + orientation constraints                       | [06](06_bonus_moveit.md)       |

## The workflow for every task

```bash
# Terminal 1: start the simulated arm (RViz opens in the Desktop tab)
ros2 launch so100_bringup arm.launch.py

# Terminal 2: edit your code, then
cb                                                    # build
pytest src/so100_labs/test/test_task2_trajectories.py # fast checks of your functions
ros2 run so100_labs task2_trajectories                # watch it move in RViz
```

When the tests pass, push. GitHub runs the same unit tests **and** a simulation test for every task,
and shows "Task N ✓/✗" next to your commit (Actions tab).

Run the simulation test yourself (it starts its own simulated arm, so close terminal 1 first):

```bash
SO100_SIM_TESTS=1 pytest src/so100_labs/test/integration -k task2 -v
```

## Backends: same code, three worlds

| Command                                   | What runs                                      | Use it for                                            |
| ----------------------------------------- | ---------------------------------------------- | ----------------------------------------------------- |
| `arm.launch.py` (default `backend:=mock`) | perfect, instant "robot", RViz only            | developing and debugging                              |
| `arm.launch.py backend:=gazebo`           | physics: gravity, contacts, a table and a cube | checking it works with physics, Task 5                |
| `arm.launch.py backend:=real robot:=<id>` | the real SO-100 (lab PC only)                  | the final test, see [REAL_ROBOT.md](../REAL_ROBOT.md) |

Add `gazebo_gui:=true` to see the Gazebo window (slow without a graphics card: RViz shows the same
robot faster).

## Coordinate frame

All positions are in **`base_link`**, in metres: **z up**, and at `shoulder_pan = 0` the arm reaches
towards **−y**. The point you control is **`tcp_link`**, the tool centre point between the
fingertips. Both frames are shown in RViz.

## Useful commands

```bash
ros2 topic echo /joint_states                    # current joint angles
ros2 control list_controllers                    # which controllers are active
ros2 run tf2_ros tf2_echo base_link tcp_link     # where is the gripper?
ros2 run rqt_joint_trajectory_controller rqt_joint_trajectory_controller   # sliders
```

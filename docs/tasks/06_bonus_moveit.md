# Bonus: MoveIt and orientation constraints

MoveIt is the standard ROS motion-planning framework. It plans collision-free paths, solves IK and
time-parametrises trajectories, which is everything you built by hand in Tasks 2–5. Here it runs
**on top of the same controllers** as your labs, so it also works in Gazebo and on the real arm.

```bash
ros2 launch so100_bringup arm.launch.py rviz:=false      # terminal 1 (add backend:=gazebo if you like)
ros2 launch so100_bringup moveit.launch.py               # terminal 2: move_group + RViz
#   with Gazebo: ros2 launch so100_bringup moveit.launch.py use_sim_time:=true
```

In RViz, drag the interactive marker at the gripper and click **Plan & Execute**. The planning group
`manipulator` ends at `tcp_link`, the gripping point you used in Tasks 3–5.

## Position and orientation goals

```bash
ros2 run so100_labs bonus_moveit_goals                   # terminal 3
```

`so100_labs/bonus_moveit_goals.py` sends three goals for the same point:

| Goal | Constraints                             | Typical result                                                  |
| ---- | --------------------------------------- | --------------------------------------------------------------- |
| 1    | position only                           | ✅ reached, gripper tilted ~30°. MoveIt picks _any_ orientation |
| 2    | position + pointing down, free spin     | ✅ reached, gripper within ~3° of vertical                      |
| 3    | position + pointing sideways, free spin | ❌ fails: impossible with 5 joints                              |

Goal 3 fails because `shoulder_pan` chooses a vertical plane, the lift, elbow and wrist joints move
inside it, and `wrist_roll` only spins about the approach axis. The gripper can only point in
directions within that plane. That's why Task 4 solves for **xyz + pitch**: exactly the 4 things the
first 4 joints can control.

### Writing an `OrientationConstraint`

```python
oc = OrientationConstraint()
oc.header.frame_id = 'base_link'
oc.link_name = 'tcp_link'
oc.orientation = Quaternion(x=0.7071, y=0.0, z=0.0, w=0.7071)  # fingers (link -y) point down (base -z)
oc.absolute_x_axis_tolerance = 0.1
oc.absolute_y_axis_tolerance = 0.1
oc.absolute_z_axis_tolerance = math.pi                         # free spin about base z = approach axis
oc.parameterization = OrientationConstraint.ROTATION_VECTOR
oc.weight = 1.0
```

> ⚠️ The tolerances are about the axes of the **header frame** (`base_link`), _not_ the link's own
> axes. To allow free spin about the approach direction, put π on the base axis that is parallel to
> it: pointing down → z, pointing along base x → x.

Combine it with a `PositionConstraint` (a small sphere around the target) in a
`moveit_msgs/Constraints`, and send it as a goal (`goal_constraints`) or as a path constraint
(`path_constraints`: the orientation must hold during the _whole_ motion, which is slower to plan).

`config/moveit_kinematics.yaml` sets `position_only_ik: true`. IK solves for the position, and the
orientation is enforced by your constraint. With full-pose IK, almost every goal would fail on a
5-joint arm.

## Things to try

- Tighten goal 2's tolerances to 0.02 rad. What happens to planning time and success rate?
- Use goal 2 as a **path** constraint and compare the motion with and without it.
- In RViz's _Planning_ tab, try different planners (RRTConnect, PRM, …) and compare the paths.
- Re-do Task 5's pick-and-place with MoveIt goals. Which parts get easier, and which harder?

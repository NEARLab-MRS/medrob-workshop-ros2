# Bonus: MoveIt

MoveIt is the standard ROS motion-planning framework. It plans collision-free paths, solves IK and
time-parametrises trajectories, which is everything you built by hand in Tasks 2–5.

```bash
ros2 launch so_arm100_moveit_config demo.launch.py hardware_type:=mock_components
```

In RViz, drag the interactive marker at the gripper and click **Plan & Execute**.

Things to try:

- Compare MoveIt's path to the same goal with your Task 4 joint-space move.
- In the _Planning_ tab, pick a different planner (e.g. RRTConnect vs PRM) and compare the paths.
- Write a node that sends a goal to MoveIt with `moveit_py` (MoveItPy) or the `MoveGroup` action.

(This demo starts its own controllers. Stop `arm.launch.py` first.)

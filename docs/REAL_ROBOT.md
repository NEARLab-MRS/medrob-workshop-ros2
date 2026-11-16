# Running your code on the real SO-100

The real robot runs on a **lab PC** (Linux) in the _same_ container as your codespace. Your code
does not change: only the launch command does.

> ⚠️ **Safety rules (every session)**
>
> 1. Clear the area around the arm. Nothing within 40 cm, including your face.
> 2. Keep one hand near the **power switch** while the arm moves. It is the real emergency stop.
> 3. Your code must pass its unit tests and run correctly in simulation first. The helper script
>    enforces this.
> 4. Start slow (`speed 0.3`), then go faster only if everything looks right.

## Each session

1. On the lab PC, open VS Code in your repository (clone it the first time:
   `git clone https://github.com/<you>/<your-repo>.git`), then `git pull`.
2. **Command Palette → "Dev Containers: Reopen in Container" → "SO-100 Lab PC (real robot)"**. The
   first time takes a few minutes.
3. Plug in the robot's USB and power, then check: `bash scripts/check_setup.sh`. It should report
   _Robot found at /dev/so100_.
4. Terminal 1: start the robot (use the robot ID written on your arm, e.g. `arm3`):

   ```bash
   ros2 launch so100_bringup arm.launch.py backend:=real robot:=arm3
   ```

   The arm switches torque on and holds its current pose. RViz shows the real robot.

5. Terminal 2: run a task (2–5) slowly:

   ```bash
   bash scripts/run_on_robot.sh task2          # speed 0.3 by default
   bash scripts/run_on_robot.sh task4 0.5      # faster once you trust it
   ```

6. When done: `Ctrl+C` in terminal 1, **support the arm** (it goes limp when torque turns off), then
   switch the power off.

## If something goes wrong

| Situation                                    | Action                                                                                                                                          |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Arm heading for a collision                  | **Power switch.**                                                                                                                               |
| Want to stop now, arm safe to drop           | `ros2 run so100_bringup estop` (torque off, the arm falls, so support it). Resume with `estop --resume`                                         |
| "SAFETY STOP" in terminal 1                  | The safety monitor saw a joint leave its safe range or move too fast. The trajectory was cancelled and the arm holds still. Check your targets. |
| "Trajectory too fast" / "outside [..]" error | `Arm` refused to send your command. Fix your code (it would also fail in sim).                                                                  |
| `/dev/so100` not found                       | USB cable/power; ask your instructor to check the udev rule (`ls /dev/ttyACM* /dev/ttyUSB*`)                                                    |
| Robot pose in RViz ≠ real pose               | The robot needs (re)calibration (below)                                                                                                         |

What protects the robot, in order:

1. `Arm` (in `arm.py`) checks joint limits and speed before sending anything.
2. On real hardware, `speed_scale` slows every trajectory down.
3. The `safety_monitor` node (started automatically with `backend:=real`) watches the actual joints
   and stops the trajectory if a joint goes past the tighter limits in
   `so100_bringup/config/safety_limits.yaml` or moves faster than 1.5 rad/s.
4. `forward_position_controller` (Task 1) is not available on the real robot.
5. You, with your hand on the power switch.

## Instructor: one-time lab PC setup

1. Install Docker and VS Code with the _Dev Containers_ extension. Add the lab user to the `docker`
   group.
2. From a clone of this repo: `sudo bash scripts/install_udev_rules.sh` creates the `/dev/so100`
   symlink. Replug the robot.
3. Allow the container to open windows: add `xhost +local:` to the lab user's session startup (e.g.
   `~/.xprofile`).
4. Calibrate each robot once and commit the file (see below).

### Calibration (once per robot, or after reassembly)

The servos report raw positions (0–4095). The calibration maps them to the URDF angles. Run with
**nothing else** using the robot (no `arm.launch.py`):

```bash
ros2 run so100_bringup calibrate --robot-id arm3
```

Torque turns off. Move the arm into the **zero pose**, which is the pose RViz shows when you run
`ros2 launch so100_bringup arm.launch.py` (mock) with every joint at 0. Then press Enter. The
offsets are saved to `src/so100_bringup/config/robots/arm3.yaml`. Run `cb`, then check with
`backend:=real robot:=arm3` that RViz matches the real arm when you move it to a few poses. Commit
the file to the template repo so all students get it.

> The calibration script and the Feetech driver integration are written against the
> `ros-jazzy-feetech-ros2-driver` 0.2.x apt release (software `offset` per joint). Newer driver
> versions replace `offset` with `homing_offset`. Check `dpkg -l ros-jazzy-feetech-ros2-driver` if
> calibration stops working after an image update.

# ROS 2 Student Lab: SO-100 robot arm

A complete ROS 2 Jazzy environment that runs **entirely in your browser**. Nothing to install, and
it works the same on macOS, Windows, Linux and Chromebook. You program a simulated **SO-100 robot
arm** (joint commands, trajectories, kinematics, pick-and-place) and then run the same code on the
real arm in the lab.

**You need:** a GitHub account, a modern browser (Chrome, Edge, Firefox or Safari), and a stable
internet connection.

---

## 1. Get free compute hours (do this first)

Apply for the [GitHub Student Developer Pack](https://education.github.com/pack). Approval can take
a few days, so don't wait until the first lab. Without it you still get a smaller free monthly
allowance.

## 2. Create your lab environment

1. Click **Use this template → Create a new repository** at the top of this page. Name it, e.g.,
   `ros2-lab-yourname`.
2. In your new repository, click **Code → Codespaces → Create codespace on main**.
3. Wait for the setup to finish. **The first launch takes a few minutes** (up to 10 if the
   prebuilt image isn't available); later launches take under a minute.
4. When the terminal says `Setup complete`, open a **new terminal** (Terminal → New Terminal) and
   run:

   ```bash
   bash scripts/check_setup.sh
   ```

## 3. Open the ROS desktop

Graphical tools (turtlesim, RViz2, Gazebo) appear in a separate desktop tab:

1. Open the **PORTS** tab at the bottom of VS Code.
2. Hover over port **6080** and click the **globe icon** to open it in a new browser tab.
3. Click **Connect** and enter the password: `vscode`

Keep two browser tabs open: **VS Code** for code and terminals, **Desktop** for seeing your robots.

## 4. Try it out

Run these in the VS Code terminal and watch the Desktop tab:

```bash
# Turtle drawing a square
ros2 launch lab_starter turtle_square.launch.py

# Publisher and subscriber talking to each other
ros2 launch lab_starter talker_listener.launch.py

# Drive the turtle yourself (run each in its own terminal)
ros2 run turtlesim turtlesim_node
ros2 run turtlesim turtle_teleop_key

# 3D visualisation and simulation
rviz2
ros2 launch ros_gz_sim gz_sim.launch.py gz_args:=shapes.sdf
```

Press `Ctrl+C` in the terminal to stop a program.

## 5. Warm-up exercise (Task 0)

Open `src/lab_starter/lab_starter/turtle_circle.py` and follow the TODO. Then:

```bash
cb                                              # build (shortcut for colcon build + source)
colcon test --packages-select lab_starter       # run the tests
colcon test-result --verbose                    # see which passed
```

When you push, GitHub runs the same tests automatically. Look for the ✓ or ✗ next to your commit.

## 6. The SO-100 arm labs (Tasks 1–5)

```bash
ros2 launch so100_bringup arm.launch.py     # simulated arm; look at the Desktop tab (RViz)
```

Then follow **[docs/tasks/README.md](docs/tasks/README.md)**: five tasks from joint commands to
Cartesian pick-and-place, each with tests and a guide. When your code works in simulation, run it
on the real arm: **[docs/REAL_ROBOT.md](docs/REAL_ROBOT.md)**.

## Workspace layout

```
src/
├── so100_labs/            # ← YOUR CODE for the arm labs
│   ├── so100_labs/        #    task1_…py … task5_…py (TODOs), arm.py + robot_model.py (provided)
│   └── test/              #    unit tests + simulation tests
├── so100_bringup/         # launch files, robot config, safety tools (don't need to change)
├── lab_starter/           # turtlesim warm-up (Task 0)
└── third_party/           # SO-100 robot description from the community (don't change)
docs/                      # task guides, real-robot guide
```

## ⚠️ Save your work

- **Commit and push at the end of every session** (Source Control icon in the left sidebar → write a
  message → Commit → Sync).
- Your codespace **stops after 30 minutes idle**. Files are kept when it stops, but unused
  codespaces are **deleted after about 30 days**. Anything not pushed is then lost.
- **Stop your codespace when you're done** (github.com/codespaces → ⋯ → Stop) so you don't waste
  your monthly hours.

## Troubleshooting

| Problem                                        | Fix                                                               |
| ---------------------------------------------- | ----------------------------------------------------------------- |
| `ros2: command not found` or package not found | Open a **new** terminal, or run `cb`                              |
| Port 6080 shows nothing / connection error     | Wait 30 seconds and refresh; check the PORTS tab shows 6080       |
| Window opened but desktop is empty             | The program may still be starting; Gazebo can take 30+ seconds    |
| Gazebo is very slow                            | Normal: no graphics card. Keep `gazebo_gui:=false` (default) and watch RViz |
| `arm.launch.py`: controllers never become active | Another copy is still running. `Ctrl+C` all terminals, then relaunch |
| Task says "No /joint_states received"         | Start `ros2 launch so100_bringup arm.launch.py` in another terminal first |
| "Codespace usage limit reached"                | You've used your monthly hours. Contact your instructor           |
| Something is badly broken                      | Commit/push your code, delete the codespace, create a fresh one   |

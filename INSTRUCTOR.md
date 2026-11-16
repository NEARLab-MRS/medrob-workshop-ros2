# Instructor Guide

## One-time setup

1. **Push this repo to GitHub** (ideally in a course organization) and enable **Settings → General →
   Template repository**.
2. **Test it as a student would.** Create a codespace from a test account and run through README
   steps 2–6, including `arm.launch.py` with `backend:=mock` and `backend:=gazebo`.
3. **Make the prebuilt image public (required for fast starts).** The *Build dev container
   image* workflow pushes `ghcr.io/bfortuno/ros2-student-lab:jazzy` (full environment including
   the desktop). `devcontainer.json` uses it as a build cache, so codespaces start in ~1–2 minutes
   instead of ~10. GitHub creates the package as **private**, so students can't pull it. Once,
   after the first run: github.com → your profile → **Packages → ros2-student-lab → Package
   settings → Change visibility → Public**. The image is rebuilt weekly and whenever
   `.devcontainer/` changes.
   *Alternative:* Codespaces prebuilds (**Settings → Codespaces → Set up prebuild**) also work,
   but their storage is billed to the repo owner.
4. **Ask students to apply for GitHub Education** at least 3 weeks before the first lab.

## Distribution options

- **Simple:** share the template link; students click "Use this template".
- **GitHub Classroom:** create an assignment from this template. Each student gets a private copy
  you can view, and Classroom can use the included tests for autograding. Verified teachers can also
  get Codespaces usage covered for the classroom organization; check the current terms on GitHub
  Education.

## Compute budget

Codespaces usage is counted in core-hours. The config requests a 4-core machine (16 GB RAM), which
Gazebo needs. That machine uses 4 core-hours per real hour:

| Account                   | Monthly allowance (check current terms) | Hours on 4-core |
| ------------------------- | --------------------------------------- | --------------- |
| Free                      | 120 core-hours                          | ~30 h           |
| Student Pack (GitHub Pro) | 180 core-hours                          | ~45 h           |

If your course doesn't use Gazebo, change `hostRequirements.cpus` to `2` in
`.devcontainer/devcontainer.json` to double students' available hours.

## SO-100 arm labs

- Packages: `so100_bringup` (launch, configs, safety, calibration), `so100_labs` (student tasks and
  tests), `third_party/ros2_so_arm100` (vendored robot description, see `VENDORED.md`).
- One launch file for everything: `ros2 launch so100_bringup arm.launch.py
  backend:=mock|gazebo|real controller:=trajectory|position`.
- **Grading:** `.github/workflows/test.yml` runs one job per task (unit tests + a headless
  simulation test with mock hardware), so each commit shows "Task N ✓/✗". With GitHub Classroom,
  use these job results for autograding, or add a `classroom.yml` that runs the same pytest
  commands. The starter repo shows ✗ for every task by design.
- **Reference solutions** are kept **outside** this public repo (the solution files replace
  `src/so100_labs/so100_labs/task*.py`). Verify with:
  `cp <solutions>/so100_labs/task*.py src/so100_labs/so100_labs/ && cb && pytest src/so100_labs/test
  && SO100_SIM_TESTS=1 pytest src/so100_labs/test/integration`, then `git checkout` the stubs
  again.
- **Real robot:** lab PCs run `.devcontainer/lab-pc/` (USB + host display). Setup, calibration
  and safety layers are in [docs/REAL_ROBOT.md](docs/REAL_ROBOT.md). Commit one calibration file
  per robot in `src/so100_bringup/config/robots/`. The safety limits are in
  `src/so100_bringup/config/safety_limits.yaml`.
- **Gazebo:** the table world (`so100_bringup/worlds/table.sdf`) has a cube for Task 5. Grasping
  works through the finger collision pads added in `so100_bringup/urdf/so100.urdf.xacro` (the
  upstream model has no gripper collisions).

## Customizing

- **Add ROS packages:** add `ros-jazzy-<name>` to the `apt-get install` line in
  `.devcontainer/Dockerfile` (e.g., `ros-jazzy-navigation2 ros-jazzy-nav2-bringup`,
  `ros-jazzy-turtlebot3*`, `ros-jazzy-moveit`), or declare them in a `package.xml` so `rosdep`
  installs them on create.
- **Add new labs:** add a `taskN_*.py` in `src/so100_labs/so100_labs/`, register it under
  `console_scripts` in `setup.py`, add `test/test_taskN_*.py` and a `test_taskN_*` function in
  `test/integration/test_sim_tasks.py`, then add a row to the matrix in `.github/workflows/test.yml`.
- **Change the desktop password:** edit `password` under the `desktop-lite` feature.
- After changing anything in `.devcontainer/`, rebuild with Command Palette → "Codespaces: Rebuild
  Container", and re-run the prebuild.

## How it works

- `Dockerfile`: official `osrf/ros:jazzy-desktop-full` image (ROS 2, RViz2, turtlesim) plus Gazebo
  Harmonic, ros2_control, MoveIt and the Feetech servo driver.
- `desktop-lite` feature: lightweight Linux desktop served through noVNC on port 6080.
- `post-create.sh`: installs dependencies with rosdep, builds the workspace, and sets up `~/.bashrc`
  (including the `cb` build shortcut).
- `sshd` feature: lets you (or a TA) open a terminal in a student's codespace via
  `gh codespace ssh`.
- `.github/workflows/test.yml`: builds and tests every task on every push. All tasks fail until
  students complete the TODOs, so the starter repo shows a red ✗ by design.
- `.github/workflows/image.yml`: prebuilds the dev container image (only in this repo, not in
  student copies).

## Known limitations

- No GPU: simple Gazebo worlds and RViz2 work; camera-heavy or multi-robot simulations will be slow.
- Students need a stable connection; the desktop tab streams over VNC.
- Codespaces stop after 30 minutes idle (configurable per user up to 4 hours in
  github.com/settings/codespaces).

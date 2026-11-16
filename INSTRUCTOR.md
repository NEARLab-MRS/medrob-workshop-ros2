# Instructor Guide

## One-time setup

1. **Push this repo to GitHub** (ideally in a course organization) and enable
   **Settings → General → Template repository**.
2. **Test it as a student would.** Create a codespace from a test account and run
   through README steps 2–4, including `rviz2` and the Gazebo `shapes.sdf` world.
3. **Enable prebuilds (strongly recommended).** Repository **Settings → Codespaces →
   Set up prebuild**, branch `main`, 4-core machine. This cuts first launch from
   ~5–10 minutes to ~1 minute. Prebuild storage is billed to the repo owner, so
   check your organization's Codespaces budget.
4. **Ask students to apply for GitHub Education** at least 3 weeks before the first lab.

## Distribution options

- **Simple:** share the template link; students click "Use this template".
- **GitHub Classroom:** create an assignment from this template. Each student gets a
  private copy you can view, and Classroom can use the included tests for
  autograding. Verified teachers can also get Codespaces usage covered for the
  classroom organization; check the current terms on GitHub Education.

## Compute budget

Codespaces usage is counted in core-hours. The config requests a 4-core machine
(16 GB RAM), which Gazebo needs. That machine uses 4 core-hours per real hour:

| Account | Monthly allowance (check current terms) | Hours on 4-core |
|---|---|---|
| Free | 120 core-hours | ~30 h |
| Student Pack (GitHub Pro) | 180 core-hours | ~45 h |

If your course doesn't use Gazebo, change `hostRequirements.cpus` to `2` in
`.devcontainer/devcontainer.json` to double students' available hours.

## Customizing

- **Add ROS packages:** add `ros-jazzy-<name>` to the `apt-get install` line in
  `.devcontainer/Dockerfile` (e.g., `ros-jazzy-navigation2 ros-jazzy-nav2-bringup`,
  `ros-jazzy-turtlebot3*`, `ros-jazzy-moveit`), or declare them in a `package.xml`
  so `rosdep` installs them on create.
- **Add new labs:** add nodes in `src/lab_starter/lab_starter/`, register them under
  `console_scripts` in `setup.py`, and add tests in `src/lab_starter/test/`.
- **Change the desktop password:** edit `password` under the `desktop-lite` feature.
- After changing anything in `.devcontainer/`, rebuild with Command Palette →
  "Codespaces: Rebuild Container", and re-run the prebuild.

## How it works

- `Dockerfile`: official `osrf/ros:jazzy-desktop-full` image (ROS 2, RViz2,
  turtlesim) plus Gazebo Harmonic via `ros-jazzy-ros-gz`.
- `desktop-lite` feature: lightweight Linux desktop served through noVNC on port 6080.
- `post-create.sh`: installs dependencies with rosdep, builds the workspace, and
  sets up `~/.bashrc` (including the `cb` build shortcut).
- `.github/workflows/test.yml`: builds and tests on every push. Note that the
  circle-exercise tests fail until students complete the TODO, so the starter
  repo shows a red ✗ by design.

## Known limitations

- No GPU: simple Gazebo worlds and RViz2 work; camera-heavy or multi-robot
  simulations will be slow.
- Students need a stable connection; the desktop tab streams over VNC.
- Codespaces stop after 30 minutes idle (configurable per user up to 4 hours in
  github.com/settings/codespaces).

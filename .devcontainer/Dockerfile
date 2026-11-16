# ROS 2 Jazzy + Gazebo Harmonic, for GitHub Codespaces
FROM osrf/ros:jazzy-desktop-full

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        sudo git nano less python3-pip python3-pytest \
        ros-jazzy-turtlesim ros-jazzy-ros-gz ros-jazzy-rqt-graph \
    && rm -rf /var/lib/apt/lists/*

# The Ubuntu 24.04 base image ships a non-root "ubuntu" user (uid 1000).
# Give it passwordless sudo so students can install extra packages if needed.
RUN echo "ubuntu ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ubuntu \
    && chmod 0440 /etc/sudoers.d/ubuntu

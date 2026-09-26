# VNAV LAB2 - Two-Drone TF2 Package

This ROS Noetic catkin package publishes and visualizes two time-varying drone
frames. AV1 follows a unit circle with yaw equal to elapsed time. AV2 follows a
parabolic arc in the world x-z plane. The plotting node uses TF2 lookups to
display both world trajectories and the trajectory of AV2 expressed in AV1.

## Build

```bash
cd ~/vnav_ws
source /opt/ros/noetic/setup.bash
catkin build
source devel/setup.bash
```

## Run

Static scenario:

```bash
roslaunch two_drones_pkg two_drones.launch static:=True
```

Dynamic scenario:

```bash
roslaunch two_drones_pkg two_drones.launch
```

## Validate

With the dynamic scenario running:

```bash
python3 ~/vnav_ws/src/two_drones_pkg/test/validate_transforms.py
```

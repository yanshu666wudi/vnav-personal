# LAB2 - ROS Installation and Use

This folder contains the completed ROS Noetic two-drone assignment, the
mathematical answers, the validation script, and the English experimental
report.

## Contents

- `two_drones_pkg/`: complete ROS 1 catkin package.
- `deliverable_answers.md`: answers for Deliverables 1-6.
- `report/lab2_report.tex`: English report source.
- `report/LAB2_Report_Li_Yunzhe.pdf`: compiled English report.
- `report/figures/`: report figures generated from the analytical equations and
  measured validation results.

## Build

ROS Noetic and catkin tools are required. Place `two_drones_pkg` in the `src`
directory of a catkin workspace, then run:

```bash
cd ~/vnav_ws
source /opt/ros/noetic/setup.bash
catkin build
source devel/setup.bash
```

## Static and dynamic scenarios

Static transforms:

```bash
roslaunch two_drones_pkg two_drones.launch static:=True
```

Dynamic transforms:

```bash
roslaunch two_drones_pkg two_drones.launch
```

The RViz configuration already includes the TF display, the drone meshes, and
the three trajectory trails.

## Validation

Keep the dynamic scenario running, then execute:

```bash
python3 ~/vnav_ws/src/two_drones_pkg/test/validate_transforms.py
```

The completed run used 40 synchronized samples and returned `PASS`. The
measured `/tf` publication rate was 50.000 Hz.

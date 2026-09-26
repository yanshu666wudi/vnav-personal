# LAB2 Deliverable Answers

## Deliverable 1 - Nodes, topics, and launch files

### 1. Nodes in the static scenario

Ignoring `/rosout`, the running nodes are:

- `/av1broadcaster`
- `/av2broadcaster`
- `/plots_publisher_node`
- `/rviz`

### 2. Equivalent static scenario without `roslaunch`

Start each line in a separate sourced terminal:

```bash
roscore
```

```bash
rosrun tf2_ros static_transform_publisher 1 0 0 0 0 0 1 world av1 __name:=av1broadcaster
```

```bash
rosrun tf2_ros static_transform_publisher 0 0 1 0 0 0 1 world av2 __name:=av2broadcaster
```

```bash
rosrun two_drones_pkg plots_publisher_node
```

```bash
rosrun rviz rviz -d "$(rospack find two_drones_pkg)/config/default.rviz"
```

### 3. Publishers and subscribers

| Node | Publishes | Subscribes | Role |
|---|---|---|---|
| `/av1broadcaster` | `/tf_static`, `/rosout` | none | Publishes the fixed `world -> av1` frame |
| `/av2broadcaster` | `/tf_static`, `/rosout` | none | Publishes the fixed `world -> av2` frame |
| `/plots_publisher_node` | `/visuals`, `/rosout` | `/tf`, `/tf_static` | Looks up transforms and creates meshes/trails |
| `/rviz` | GUI interaction topics and `/rosout` | `/tf`, `/tf_static`, `/visuals` | Displays frames, meshes, and trails |

The two static broadcasters publish the AV1 and AV2 frames. The plotting node
publishes the drone mesh markers and trajectory markers on `/visuals`; this is
the topic that makes the two drone meshes appear in RViz.

### 4. Effect of omitting `static:=True`

The launch argument has the default value `false`. The group containing the two
static broadcasters uses `if="$(arg static)"`, so it is disabled when the
argument is omitted. The dynamic frame node uses
`unless="$(arg static)"`, so it is enabled. The result is that a single
`frames_publisher_node` publishes moving `world -> av1` and `world -> av2`
transforms on `/tf` at 50 Hz.

## Deliverable 2 - Publishing transforms

The completed frame publisher uses elapsed time `t` and publishes:

\[
o_1^w(t)=[\cos t,\sin t,0]^T, \qquad
o_2^w(t)=[\sin t,0,\cos(2t)]^T.
\]

AV1 uses roll = 0, pitch = 0, yaw = `t`. AV2 uses identity orientation. Both
transforms share one time stamp and are sent together by a
`tf2_ros::TransformBroadcaster` every 0.02 s.

## Deliverable 3 - Looking up transforms

Each trajectory trail retrieves the latest pose with:

```cpp
transform = parent->tf_buffer.lookupTransform(
    ref_frame, dest_frame, ros::Time(0), ros::Duration(0.02));
```

This produces the AV1 world trail, AV2 world trail, and AV2-in-AV1 trail.

## Deliverable 4 - Mathematical derivations

The complete derivation is typeset in the report. The final results are:

1. AV2 in the world frame satisfies
   \[
   y_2^w=0, \qquad z_2^w=1-2(x_2^w)^2,
   \]
   so it is a parabola in the world `x-z` plane.
2. AV2 expressed in AV1 is
   \[
   o_2^1(t)=[\cos t\sin t-1,-\sin^2t,\cos(2t)]^T.
   \]
3. The relative curve lies on
   \[
   \Pi: 2y_2^1-z_2^1+1=0.
   \]
4. With origin `p^1=(-1,-1/2,0)^T` and the orthonormal axes
   \[
   e_{x_p}=[1,0,0]^T,\quad
   e_{y_p}=[0,1,2]^T/\sqrt5,\quad
   e_{z_p}=[0,-2,1]^T/\sqrt5,
   \]
   the centered coordinates are
   \[
   x_p=\tfrac12\sin(2t),\qquad
   y_p=\tfrac{\sqrt5}{2}\cos(2t),\qquad z_p=0.
   \]
5. Therefore
   \[
   \frac{x_p^2}{(1/2)^2}+\frac{y_p^2}{(\sqrt5/2)^2}=1,
   \]
   and the semi-axis lengths are `1/2` and `sqrt(5)/2`.

## Deliverable 5 - Quaternion properties

For a unit quaternion `q`, quaternion norm multiplicativity shows that left and
right multiplication preserve every vector norm. Therefore both
`Omega_1(q)` and `Omega_2(q)` are orthogonal. Their transposes represent
multiplication by the inverse quaternion, which gives

\[
\Omega_1(q)^Tq=\Omega_2(q)^Tq=[0,0,0,1]^T.
\]

Associativity proves that left and right multiplication commute. Since
`Omega_2(y)^T=Omega_2(y*)`, the same argument proves commutation with the
transpose.

## Optional Deliverable 6 - Intrinsic and extrinsic rotations

A fixed-axis rotation pre-multiplies the current attitude, while a moving-axis
rotation post-multiplies it. Thus an extrinsic sequence `A0, A1, ..., An` gives
`An ... A1 A0`, and the reversed intrinsic sequence `An, ..., A1, A0` gives the
same matrix.

## Verification results

- Catkin build: 1 package succeeded, 0 warnings, 0 failures.
- `/tf` rate: 50.000 Hz.
- 40 synchronized transform samples: PASS.
- Maximum AV1 radius error: `2.220e-16`.
- Maximum AV2 world-trajectory error: `2.989e-16`.
- Maximum AV1 yaw error: `4.441e-16`.
- Maximum relative-position error: `8.083e-16`.

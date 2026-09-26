#!/usr/bin/env python3

import math

import rospy
import tf2_ros
from tf.transformations import euler_from_quaternion


def angle_error(first_angle, second_angle):
    return abs(math.atan2(math.sin(first_angle - second_angle),
                          math.cos(first_angle - second_angle)))


def vector_error(measured_values, expected_values):
    return math.sqrt(sum((measured_value - expected_value) ** 2
                         for measured_value, expected_value
                         in zip(measured_values, expected_values)))


def main():
    rospy.init_node("validate_two_drones_transforms", anonymous=True)
    transform_buffer = tf2_ros.Buffer(cache_time=rospy.Duration(10.0))
    transform_listener = tf2_ros.TransformListener(transform_buffer)
    rospy.sleep(1.0)

    maximum_radius_error = 0.0
    maximum_av2_error = 0.0
    maximum_yaw_error = 0.0
    maximum_relative_error = 0.0

    for _ in range(40):
        av1_world = transform_buffer.lookup_transform(
            "world", "av1", rospy.Time(0), rospy.Duration(1.0))
        sample_time = av1_world.header.stamp
        av2_world = transform_buffer.lookup_transform(
            "world", "av2", sample_time, rospy.Duration(1.0))
        av2_av1 = transform_buffer.lookup_transform(
            "av1", "av2", sample_time, rospy.Duration(1.0))

        av1_x = av1_world.transform.translation.x
        av1_y = av1_world.transform.translation.y
        trajectory_time = math.atan2(av1_y, av1_x)
        sine_time = math.sin(trajectory_time)
        cosine_time = math.cos(trajectory_time)

        maximum_radius_error = max(
            maximum_radius_error,
            abs(math.hypot(av1_x, av1_y) - 1.0))

        expected_av2 = (
            sine_time,
            0.0,
            math.cos(2.0 * trajectory_time),
        )
        measured_av2 = (
            av2_world.transform.translation.x,
            av2_world.transform.translation.y,
            av2_world.transform.translation.z,
        )
        maximum_av2_error = max(
            maximum_av2_error,
            vector_error(measured_av2, expected_av2))

        orientation = av1_world.transform.rotation
        measured_yaw = euler_from_quaternion(
            [orientation.x, orientation.y, orientation.z, orientation.w])[2]
        maximum_yaw_error = max(
            maximum_yaw_error,
            angle_error(measured_yaw, trajectory_time))

        expected_relative = (
            cosine_time * sine_time - 1.0,
            -(sine_time ** 2),
            math.cos(2.0 * trajectory_time),
        )
        measured_relative = (
            av2_av1.transform.translation.x,
            av2_av1.transform.translation.y,
            av2_av1.transform.translation.z,
        )
        maximum_relative_error = max(
            maximum_relative_error,
            vector_error(measured_relative, expected_relative))
        rospy.sleep(0.05)

    tolerance = 1.0e-3
    test_passed = all(error <= tolerance for error in (
        maximum_radius_error,
        maximum_av2_error,
        maximum_yaw_error,
        maximum_relative_error,
    ))

    print("Two-drones transform validation")
    print("  samples: 40")
    print("  max AV1 radius error:     {:.3e}".format(maximum_radius_error))
    print("  max AV2 trajectory error: {:.3e}".format(maximum_av2_error))
    print("  max AV1 yaw error:        {:.3e}".format(maximum_yaw_error))
    print("  max relative pose error:  {:.3e}".format(maximum_relative_error))
    print("  result: {}".format("PASS" if test_passed else "FAIL"))

    if not test_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


output_directory = Path(__file__).resolve().parent / "figures"
output_directory.mkdir(parents=True, exist_ok=True)


def save_figure(figure, filename):
    figure.savefig(output_directory / f"{filename}.pdf", bbox_inches="tight")
    figure.savefig(output_directory / f"{filename}.png", dpi=220,
                   bbox_inches="tight")
    plt.close(figure)


def create_world_trajectory_figure():
    trajectory_time = np.linspace(0.0, 2.0 * np.pi, 600)
    av1_x = np.cos(trajectory_time)
    av1_y = np.sin(trajectory_time)
    av1_z = np.zeros_like(trajectory_time)
    av2_x = np.sin(trajectory_time)
    av2_y = np.zeros_like(trajectory_time)
    av2_z = np.cos(2.0 * trajectory_time)

    figure = plt.figure(figsize=(8.8, 4.2))
    axis_3d = figure.add_subplot(121, projection="3d")
    axis_3d.plot(av1_x, av1_y, av1_z, color="#1565c0", linewidth=2.4,
                 label="AV1: circle")
    axis_3d.plot(av2_x, av2_y, av2_z, color="#d95f02", linewidth=2.4,
                 linestyle="--", label="AV2: parabola")
    axis_3d.scatter([1.0], [0.0], [0.0], color="#1565c0", marker="o")
    axis_3d.scatter([0.0], [0.0], [1.0], color="#d95f02", marker="s")
    axis_3d.set_xlabel("$x_w$ [m]")
    axis_3d.set_ylabel("$y_w$ [m]")
    axis_3d.set_zlabel("$z_w$ [m]")
    axis_3d.set_title("World-frame trajectories")
    axis_3d.view_init(elev=24, azim=-52)
    axis_3d.legend(loc="upper left", fontsize=8)

    axis_xz = figure.add_subplot(122)
    axis_xz.plot(av2_x, av2_z, color="#d95f02", linewidth=2.5,
                 label="$z_w=1-2x_w^2$")
    axis_xz.scatter([0.0], [1.0], color="#d95f02", marker="s",
                    label="Initial position")
    axis_xz.set_xlabel("$x_w$ [m]")
    axis_xz.set_ylabel("$z_w$ [m]")
    axis_xz.set_title("AV2 projected onto the $x_w$-$z_w$ plane")
    axis_xz.grid(alpha=0.25)
    axis_xz.set_aspect("equal", adjustable="box")
    axis_xz.legend(fontsize=8)
    figure.tight_layout()
    save_figure(figure, "world_trajectories")


def create_relative_trajectory_figure():
    trajectory_time = np.linspace(0.0, 2.0 * np.pi, 600)
    sine_time = np.sin(trajectory_time)
    cosine_time = np.cos(trajectory_time)
    relative_x = cosine_time * sine_time - 1.0
    relative_y = -(sine_time ** 2)
    relative_z = np.cos(2.0 * trajectory_time)
    plane_x = 0.5 * np.sin(2.0 * trajectory_time)
    plane_y = math.sqrt(5.0) / 2.0 * np.cos(2.0 * trajectory_time)

    figure = plt.figure(figsize=(8.8, 4.2))
    axis_3d = figure.add_subplot(121, projection="3d")
    axis_3d.plot(relative_x, relative_y, relative_z, color="#6a3d9a",
                 linewidth=2.5)
    axis_3d.scatter([-1.0], [-0.5], [0.0], color="black", marker="x",
                    s=50, label="Center $p^1$")
    axis_3d.set_xlabel("$x_2^1$ [m]")
    axis_3d.set_ylabel("$y_2^1$ [m]")
    axis_3d.set_zlabel("$z_2^1$ [m]")
    axis_3d.set_title("AV2 observed in the AV1 frame")
    axis_3d.view_init(elev=25, azim=-55)
    axis_3d.legend(fontsize=8)

    axis_plane = figure.add_subplot(122)
    axis_plane.plot(plane_x, plane_y, color="#6a3d9a", linewidth=2.5,
                    label="Relative trajectory")
    axis_plane.axhline(0.0, color="0.55", linewidth=0.8)
    axis_plane.axvline(0.0, color="0.55", linewidth=0.8)
    axis_plane.scatter([0.0], [0.0], color="black", marker="x", s=50)
    axis_plane.set_xlabel("$x_p$ [m]")
    axis_plane.set_ylabel("$y_p$ [m]")
    axis_plane.set_title("Centered plane coordinates")
    axis_plane.set_aspect("equal", adjustable="box")
    axis_plane.grid(alpha=0.25)
    axis_plane.text(0.02, 0.97,
                    r"$x_p^2/(1/2)^2+y_p^2/(\sqrt{5}/2)^2=1$",
                    transform=axis_plane.transAxes, va="top", fontsize=9)
    figure.tight_layout()
    save_figure(figure, "relative_trajectory")


def add_box(axis, x_coordinate, y_coordinate, width, height, title, subtitle,
            face_color):
    box = FancyBboxPatch(
        (x_coordinate, y_coordinate), width, height,
        boxstyle="round,pad=0.02,rounding_size=0.025",
        linewidth=1.3, edgecolor="#263238", facecolor=face_color)
    axis.add_patch(box)
    axis.text(x_coordinate + width / 2.0, y_coordinate + height * 0.64,
              title, ha="center", va="center", fontsize=10,
              fontweight="bold")
    axis.text(x_coordinate + width / 2.0, y_coordinate + height * 0.30,
              subtitle, ha="center", va="center", fontsize=8.2)


def add_arrow(axis, start, end, label, color="#37474f"):
    arrow = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=13,
                            linewidth=1.5, color=color,
                            connectionstyle="arc3,rad=0.0")
    axis.add_patch(arrow)
    axis.text((start[0] + end[0]) / 2.0,
              (start[1] + end[1]) / 2.0 + 0.035,
              label, ha="center", va="bottom", fontsize=8, color=color)


def create_system_graph_figure():
    figure, axis = plt.subplots(figsize=(9.2, 4.1))
    axis.set_xlim(0.0, 1.0)
    axis.set_ylim(0.0, 1.0)
    axis.axis("off")

    add_box(axis, 0.04, 0.62, 0.23, 0.22, "frames_publisher_node",
            "Computes AV1 and AV2 poses\nat 50 Hz", "#d9ecff")
    add_box(axis, 0.39, 0.62, 0.23, 0.22, "TF2 buffer/listener",
            "Stores time-stamped\nframe transforms", "#e5f5e0")
    add_box(axis, 0.73, 0.62, 0.23, 0.22, "plots_publisher_node",
            "Looks up poses and\nbuilds three trails", "#fff1d6")
    add_box(axis, 0.39, 0.15, 0.23, 0.22, "RViz",
            "Displays frames, meshes\nand trajectories", "#f1e5f7")

    add_arrow(axis, (0.27, 0.73), (0.39, 0.73), "/tf")
    add_arrow(axis, (0.62, 0.73), (0.73, 0.73), "lookupTransform")
    add_arrow(axis, (0.82, 0.62), (0.60, 0.36), "/visuals")
    add_arrow(axis, (0.43, 0.62), (0.48, 0.37), "/tf")
    axis.text(0.5, 0.94, "ROS computation and visualization graph",
              ha="center", va="center", fontsize=13, fontweight="bold")
    figure.tight_layout()
    save_figure(figure, "ros_system_graph")


def create_validation_figure():
    error_labels = ["AV1 radius", "AV2 path", "AV1 yaw", "Relative pose"]
    maximum_errors = np.array([2.220e-16, 2.989e-16, 4.441e-16, 8.083e-16])

    figure, axes = plt.subplots(1, 2, figsize=(8.8, 3.8))
    axes[0].barh(error_labels, maximum_errors, color="#2878b5",
                 edgecolor="#1b4f72", hatch="//")
    axes[0].axvline(1.0e-3, color="#c0392b", linestyle="--", linewidth=1.6,
                    label="Acceptance limit")
    axes[0].set_xscale("log")
    axes[0].set_xlim(1.0e-17, 1.0e-2)
    axes[0].set_xlabel("Maximum absolute/geometric error")
    axes[0].set_title("40-sample transform validation")
    axes[0].legend(fontsize=8, loc="lower right")
    axes[0].grid(axis="x", alpha=0.25)

    axes[1].bar(["Measured", "Target"], [50.000, 50.000],
                color=["#4daf4a", "#bdbdbd"], edgecolor="#37474f")
    axes[1].set_ylim(0.0, 55.0)
    axes[1].set_ylabel("TF publication rate [Hz]")
    axes[1].set_title("Dynamic transform frequency")
    for index, value in enumerate([50.000, 50.000]):
        axes[1].text(index, value + 1.0, f"{value:.3f}", ha="center",
                     fontsize=9)
    axes[1].grid(axis="y", alpha=0.25)
    figure.tight_layout()
    save_figure(figure, "validation_summary")


if __name__ == "__main__":
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 9.5,
        "axes.spines.top": False,
        "axes.spines.right": False,
    })
    create_world_trajectory_figure()
    create_relative_trajectory_figure()
    create_system_graph_figure()
    create_validation_figure()

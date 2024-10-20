from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command


def generate_launch_description():
    ld = LaunchDescription()

    r_s_p_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": Command(['xacro ', "/home/george/ros2_ws/src/arm_description/urdf/arm.urdf.xacro"])}]
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments=['-d', "/home/george/ros2_ws/src/arm_description/rviz2/config1.rviz"]
    )

    j_s_p_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui"
    )

    ld.add_action(r_s_p_node)
    ld.add_action(j_s_p_node)
    ld.add_action(rviz)
    return ld
    
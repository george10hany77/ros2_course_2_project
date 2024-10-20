from launch import LaunchDescription
import os
from ament_index_python.packages import get_package_share_path
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    ld = LaunchDescription()

    r_s_p_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        namespace="robot_2",
        parameters=[{"robot_description": Command(['xacro ', "/home/george/ros2_ws/src/arm_description/urdf/arm.urdf.xacro"])}]
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments=['-d', "/home/george/ros2_ws/src/arm_description/rviz2/config1.rviz"]
    )

    # don't add it as we will add a plugin that will do that work
    j_s_p_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        namespace="robot_2"
    )

    gazebo_world_launch_argument = DeclareLaunchArgument(
        name="world", default_value="/home/george/ros2_ws/src/my_robot_bringup/worlds/my_world.world",
        description="The path of the world passed as argument"
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory("gazebo_ros"), "launch"), "/gazebo.launch.py"])
    )

    gazebo_spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=['-topic', 'robot_description',
                  '-entity', 'arm_gogo', '-z','1.0'],
        namespace="robot_2",
        output="screen"
    )

    # ld.add_action(gazebo_world_launch_argument)
    ld.add_action(r_s_p_node)
    # ld.add_action(j_s_p_node)
    # ld.add_action(gazebo)
    ld.add_action(gazebo_spawn_entity)
    # ld.add_action(rviz)
    return ld
    
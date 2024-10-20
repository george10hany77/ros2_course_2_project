from launch_ros.actions import Node
from launch import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    ld = LaunchDescription()

    robot_1 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(["/home/george/ros2_ws/src/my_robot_bringup/launch/my_robot_gazebo_2.launch.py"])
    )

    robot_2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(["/home/george/ros2_ws/src/my_robot_bringup/launch/arm_gogo_gazebo.launch.py"])
    )
 
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory("gazebo_ros"), "launch"), "/gazebo.launch.py"])
    ) 

    gazebo_world_launch_argument = DeclareLaunchArgument(
        name="world", default_value="/home/george/ros2_ws/src/my_robot_bringup/worlds/my_world.world",
        description="The path of the world passed as argument"
    )

    ld.add_action(gazebo_world_launch_argument)
    ld.add_action(gazebo)
    ld.add_action(robot_2)
    ld.add_action(robot_1)
    return ld
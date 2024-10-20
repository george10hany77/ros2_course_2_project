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
    urdf_path = os.path.join(get_package_share_path('my_robot_description'), 'urdf', 'my_urdf.urdf.xacro')
    rviz2_config_path = os.path.join(get_package_share_path('my_robot_bringup'), 'rviz2', 'config1.rviz')
    robot_description = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)
    
    robot_s_p_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        namespace="robot_1",
        parameters=[{'robot_description': robot_description}]
    )

    # DON'T launch it because we will not need it even if without it the tf of the wheels will not be recognized
    # because the wheels' joints are continuous ,so we need info from the /joint_states node.
    # And without any controller or j_s_p_gui node the tf of the wheel will have problems.
    # So we don't publish it and we let the controller node publishes the correct tf.
    joint_s_p_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        namespace="robot_1"
    )

    # to launch gazebo with the saved world 
    # the argument has to be named "world" as the gazebo.launch.py expects an argumnet named "world"
    # for more info check this: https://chatgpt.com/share/670cffd2-4650-800a-a1d1-990dac388875
    gazebo_world_launch_argument = DeclareLaunchArgument(
        name="world", default_value="/home/george/ros2_ws/src/my_robot_bringup/worlds/my_world.world",
        description="The path of the world passed as argument"
    )

    #, default_value="/home/george/ros2_ws/src/my_robot_bringup/worlds/my_world.world"

    # to launch another launch file to open gazebo
    # the argument has to be named "world" as the gazebo.launch.py expects an argumnet named "world"
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory("gazebo_ros"), "launch"), "/gazebo.launch.py"])
                )

    # to spawn the robot in gazebo
    gz_spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        output="screen",
        namespace="robot_1",
        # these are arguments not parameters
        arguments=["-topic", "robot_description",
                   "-entity", "my_robot"]
    )
    rviz2_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=['-d', rviz2_config_path]
    )
    return LaunchDescription([
        robot_s_p_node,
        # joint_s_p_node,
        # gazebo_world_launch_argument,
        # gazebo,
        gz_spawn_entity,
        # rviz2_node
    ]) 
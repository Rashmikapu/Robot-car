#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import TimerAction

def generate_launch_description():
    # Get Gazebo ROS interface package
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    # Get the location for the empty world
    world_file_path = os.path.join(get_package_share_directory('bot_car'), 'worlds', 'empty_world.world')

    # Include Gazebo server launch
    gzserver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')),
        launch_arguments={'world': world_file_path}.items(),
    )

    # Include Gazebo client launch
    gzclient = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py'))
    )

    # RViz configuration
    rviz_config_file = PathJoinSubstitution(
        [FindPackageShare("bot_car"), "rviz", "/home/vigneshr/proj1_ws/src/bot_car/rviz/new_bot_car.rviz"]
    )

    # Define the RViz Node
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file],
        parameters=[{'use_sim_time': True}],
    )

    rviz_start_delay = 5.0  # Delay in seconds

    rviz_node_with_delay = TimerAction(
        period=rviz_start_delay,
        actions=[rviz_node],
    )


    # Include robot spawn launch
    pkg_bot_car = get_package_share_directory('bot_car')
    spawn_robot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_bot_car, 'launch', 'spawn_robot_ros2.launch.py')
        )
    )

    return LaunchDescription([
        gzserver,
        gzclient,
        spawn_robot,
        rviz_node_with_delay,
    ])

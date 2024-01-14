#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription,ExecuteProcess,RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import TimerAction


def generate_launch_description():

    # Get Gazebo ROS interface package
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    # Get the location for empty world
    world = os.path.join(
        get_package_share_directory('bot_car'),
        'competition','worlds',
        'competition.world'
    )

    # Launch Description to run Gazebo Server
    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={'world': world}.items()
    )

    # Launch Description to run Gazebo Client
    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        )
    )

    # Get the package directory 
    pkg_gazebo = get_package_share_directory('bot_car')

    
        # RViz configuration
    # rviz_config_file = PathJoinSubstitution(
    #     [FindPackageShare("bot_car"), "rviz", "/home/vigneshr/proj1_ws/src/bot_car/urdf/new_bot_car.rviz"]
    # )

    # # Define the RViz Node
    # rviz_node = Node(
    #     package='rviz2',
    #     executable='rviz2',
    #     name='rviz2',
    #     output='screen',
    #     arguments=['-d', rviz_config_file],
    #     parameters=[{'use_sim_time': True}],
    # )

    # rviz_start_delay = 5.0  # Delay in seconds

    # rviz_node_with_delay = TimerAction(
    #     period=rviz_start_delay,
    #     actions=[rviz_node],
    # )
    # Launch Decription to Spawn Robot Model 
    spawn_robot_world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo, 'launch',
                         'spawn_robot_ros2.launch.py'),
        )
    )

    # Launch Description 
    return LaunchDescription([
        gzserver_cmd,
        gzclient_cmd,
        spawn_robot_world,
        #rviz_node_with_delay,  
    ])

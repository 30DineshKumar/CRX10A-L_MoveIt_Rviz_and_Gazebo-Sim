import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (IncludeLaunchDescription, RegisterEventHandler,
                            SetEnvironmentVariable)
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    pkg = get_package_share_directory('crx_sim')
    ros_gz_sim = get_package_share_directory('ros_gz_sim')

    urdf_path = os.path.join(pkg, 'urdf', 'crx10ial.urdf')
    world_path = os.path.join(pkg, 'worlds', 'crx_world.sdf')
    controllers_path = os.path.join(pkg, 'config', 'controllers.yaml')

    # Insert the real controllers.yaml path into the URDF
    with open(urdf_path, 'r') as f:
        robot_description = f.read().replace(
            'CONTROLLERS_YAML_PATH', controllers_path)

    # Lets Gazebo resolve package://crx_sim/... mesh URIs
    resource_path = SetEnvironmentVariable(
        'GZ_SIM_RESOURCE_PATH', os.path.join(pkg, '..'))

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': f'-r {world_path}'}.items(),
    )

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description,
                     'use_sim_time': True}],
        output='screen',
    )

    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description',
                   '-name', 'crx10ial',
                   '-x', '-0.4', '-y', '0.0', '-z', '0.75'],
        output='screen',
    )

    clock_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
        output='screen',
    )

    jsb_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster',
                   '--controller-manager', '/controller_manager'],
        output='screen',
    )

    jtc_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_trajectory_controller',
                   '--controller-manager', '/controller_manager',
                   '--param-file', controllers_path],
        output='screen',
    )

    # Order: spawn robot -> joint_state_broadcaster -> trajectory controller
    start_jsb = RegisterEventHandler(
        OnProcessExit(target_action=spawn, on_exit=[jsb_spawner]))
    start_jtc = RegisterEventHandler(
        OnProcessExit(target_action=jsb_spawner, on_exit=[jtc_spawner]))

    return LaunchDescription([
        resource_path, gz_sim, rsp, clock_bridge, spawn,
        start_jsb, start_jtc,
    ])

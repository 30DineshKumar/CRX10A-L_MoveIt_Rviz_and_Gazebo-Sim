import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    sim_pkg = get_package_share_directory('crx_sim')
    moveit_pkg = get_package_share_directory('crx_moveit_config')

    # 1) Gazebo + robot + ros2_control controllers (what already works)
    sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(sim_pkg, 'launch', 'spawn_crx.launch.py')))

    # 2) MoveIt configuration, using the URDF from crx_sim
    moveit_config = (
        MoveItConfigsBuilder('fanuc_crx10ial', package_name='crx_moveit_config')
        .robot_description(
            file_path=os.path.join(sim_pkg, 'urdf', 'crx10ial.urdf'))
        .robot_description_semantic(file_path='config/fanuc_crx10ial.srdf')
        .trajectory_execution(file_path='config/moveit_controllers.yaml')
        .planning_pipelines(pipelines=['ompl'])
        .to_moveit_configs()
    )

    move_group = Node(
        package='moveit_ros_move_group',
        executable='move_group',
        output='screen',
        parameters=[moveit_config.to_dict(), {'use_sim_time': True}],
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', os.path.join(moveit_pkg, 'config', 'moveit.rviz')],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            moveit_config.planning_pipelines,
            moveit_config.joint_limits,
            {'use_sim_time': True},
        ],
    )

    # Wait for Gazebo and the controllers to come up before starting MoveIt
    delayed_moveit = TimerAction(period=20.0, actions=[move_group, rviz])

    return LaunchDescription([sim, delayed_moveit])

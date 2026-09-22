from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='balloon_pop_bot',
            executable='camera_node',
            name='camera_node'
        ),
        Node(
            package='balloon_pop_bot',
            executable='detection_node',
            name='detection_node'
        ),
    ])
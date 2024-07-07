import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    pkg_share = get_package_share_directory('robot_pkg')
    urdf_file = os.path.join(pkg_share, 'model', 'AGV', 'urdf', 'AGV.urdf')
    world_file = os.path.join(pkg_share, 'model', 'AGV', 'worlds', 'empty.world')
    print(f"URDF file: {urdf_file}")
    print(f"World file: {world_file}")
    
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
            launch_arguments={'world': world_file}.items(),
        ),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': open(urdf_file).read()}]
        ),
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-entity', 'AGV', '-file', urdf_file],
            output='screen'
        )
        
    ])

if __name__ == '__main__':
    generate_launch_description()
    


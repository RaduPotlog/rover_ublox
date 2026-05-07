# Copyright 2020 Open Source Robotics Foundation, Inc.
# All rights reserved.
#
# Software License Agreement (BSD License 2.0)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above
#   copyright notice, this list of conditions and the following
#   disclaimer in the documentation and/or other materials provided
#   with the distribution.
# * Neither the name of {copyright_holder} nor the names of its
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""Launch the ublox GPS node with ZED-F9P ROVER configuration."""

import os

import ament_index_python.packages
import launch
import launch_ros.actions


def generate_launch_description():
    """Generate launch description for ZED-F9P in ROVER mode."""
    
    # Get config directory
    config_directory = os.path.join(
        ament_index_python.packages.get_package_share_directory('ublox_gps'),
        'config'
    )
    
    # ✅ USE ROVER CONFIG (10Hz, Automotive, All GNSS)
    params = os.path.join(config_directory, 'zed_f9p_rover.yaml')
    
    # Log which config is being used
    print(f"[GPS] Loading ROVER config: {params}")
    
    # GPS Node with respawn enabled
    ublox_gps_node = launch_ros.actions.Node(
        package='ublox_gps',
        executable='ublox_gps_node',
        name='ublox_gps_node',
        output='both',
        parameters=[params],
        respawn=True,              # ✅ Auto-restart if node crashes
        respawn_delay=2.0          # Wait 2 seconds before restarting
    )

    return launch.LaunchDescription([
        ublox_gps_node,
        
        # Optional: Shutdown entire launch if GPS node exits
        # Comment out this section if you want only respawn without shutdown
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=ublox_gps_node,
                on_exit=[
                    launch.actions.EmitEvent(
                        event=launch.events.Shutdown()
                    )
                ],
            )
        ),
    ])
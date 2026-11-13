# CRX-MoveIt-Gazebo-Sim

A ROS 2 simulation of the **FANUC CRX-10iA/L** collaborative robot. Plan motions with **MoveIt 2** in **RViz2** and watch the same arm execute them in **Gazebo Sim**.

[Gazebo and RViz Demo]
<br><br>


<img width="1920" height="1080" alt="Screenshot From 2026-11-13 17-28-27" src="https://github.com/user-attachments/assets/65b8816c-2d33-4f96-be41-efc6561442db" />


## ✨ Features

-  **FANUC CRX-10iA/L** URDF model with meshes
-  **Gazebo Sim world** with a ground plane, table and the robot
-  **ros2_control controllers** for trajectory execution
-  **MoveIt 2 integration** using the OMPL planning pipeline and a `crx_arm` planning group
-  **Interactive planning** in RViz: drag the goal marker, plan, execute
-  **Synchronized motion**: the plan runs on the Gazebo robot (`use_sim_time` enabled)

##  Tech Stack

- ROS 2 (Python launch files)
- MoveIt 2 (`moveit_ros_move_group`, `moveit_configs_utils`)
- Gazebo Sim (`ros_gz`)
- `ros2_control`
- RViz2
- CMake / ament

##  Project Structure

```
crx_sim/
├── config/                   # Controller and simulation config
├── include/
├── launch/
│   ├── spawn_crx.launch.py   # Gazebo + robot + controllers
│   └── moveit_sim.launch.py  # Sim + MoveIt + RViz
├── meshes/                   # Robot meshes
├── src/
├── urdf/
│   └── crx10ial.urdf         # Robot description
├── worlds/
│   └── crx_world.sdf         # Gazebo world (table, ground, sun)
├── CMakeLists.txt
├── package.xml
└── LICENSE
```

The MoveIt setup lives in a separate package, `crx_moveit_config` (SRDF, controllers, RViz config).

##  Prerequisites

- Ubuntu with ROS 2 (Humble / Jazzy / your distro)
- MoveIt 2
- Gazebo Sim and `ros_gz`
- `ros2_control` and `gz_ros2_control`
- `colcon`

```bash
sudo apt install ros-$ROS_DISTRO-moveit ros-$ROS_DISTRO-ros-gz ros-$ROS_DISTRO-ros2-control ros-$ROS_DISTRO-ros2-controllers
```

> Adjust the package names to match your distro and Gazebo version.

##  Installation

```bash
cd ~/ros2_ws/src
git clone https://github.com/30DineshKumar/<30DineshKumar>.git

cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -y
colcon build
source install/setup.bash
```
## Usage

```bash
ros2 launch crx_sim moveit_sim.launch.py
```

Then in RViz:

1. Select the `crx_arm` planning group in the **MotionPlanning** panel
2. Drag the interactive marker to set a goal pose
3. Click **Plan**, then **Plan & Execute**
4. Watch the robot move in Gazebo 🎉

##  How It Works

```
RViz (MoveIt) ──plan──▶ move_group ──trajectory──▶ ros2_control ──▶ Gazebo robot
```

1. `spawn_crx.launch.py` starts Gazebo, spawns the robot and loads the controllers.
2. `moveit_sim.launch.py` builds the MoveIt configuration (URDF, SRDF, controllers, OMPL) and starts `move_group` and RViz.
3. MoveIt plans a trajectory and sends it to the controllers, which move the arm in Gazebo.

##  Future Improvements

- Add a gripper and pick-and-place
- Add objects and collision scenes
- Python/C++ MoveIt scripts for automated motion

##  Contributing

Issues and pull requests are welcome!

## 📄 License

See the [LICENSE](LICENSE) file.

## 👤 Author

**Dinesh Kumar**
GitHub: [@30DineshKumar](https://github.com/30DineshKumar)

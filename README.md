# 🐢 ROS2 Turtle Hunter

An autonomous turtle-catching simulation built with ROS 2 and Turtlesim.

!

## 📌 Project Overview

This project demonstrates an autonomous control system where a main turtle dynamically calculates the position of newly spawned target turtles and hunts them down. It showcases core ROS 2 concepts including Publisher/Subscriber communication, custom Interfaces, Service calls, and mathematical trajectory calculations.

## 🛠️ Tech Stack & Packages

- **ROS 2 Jazzy** (Ubuntu 24.04)
- Python (rclpy)
- **`turtlesim_py_pkg`**: Contains the core logic and autonomous control nodes.
- **`turtlesim_interfaces`**: Custom message and service definitions for the project.
- **`turtlesim_bringup`**: Contains the launch files to start the entire system seamlessly.

## 🚀 How to Run

1. Clone the repository into your workspace's `src` folder:

```bash
git clone [<https://github.com/aas1112/ros2-turtle-hunter.git>](<https://github.com/aas1112/ros2-turtle-hunter.git>)
```


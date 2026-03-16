#!/usr/bin/env python3
import sys
import math
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim_interfaces.msg import TurtleArray
from turtlesim_interfaces.msg import Turtle
from turtlesim_interfaces.srv import CatchTurtle
from functools import partial

class go_to_loc_node(Node):
    def __init__(self):
        super().__init__("go_to_loc_node")
        self.coeff = 1.5
        self.pose_threshold_linear = 1
        self.pose_threshold_angular = 0.01
        self.target_x = 4.0
        self.target_y = 9.0

        self.pose_ = None
        self.new_turtle_to_catch_ = None

        self.publisher_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.subscriber_ = self.create_subscription(Pose, "/turtle1/pose", self.callback_turtle_pose, 10)
        self.new_turtle_subscriber_ = self.create_subscription(TurtleArray, "new_turtles", self.callback_new_turtle, 10)
        self.timer = self.create_timer(0.01, self.turtle_controller)

        self.get_logger().info("Go to loc node started")
        
        
        

    def callback_turtle_pose(self, msg):
        self.pose_ = msg

    def callback_new_turtle(self, msg):
        if len(msg.turtles) > 0:
            self.new_turtle_to_catch_ = msg.turtles[0]

    def turtle_controller(self):
        pose = self.pose_
        target = self.new_turtle_to_catch_
        if pose is None or target is None:
            return
            
        msg = Twist()
        dist_x = target.x - pose.x
        dist_y = target.y - pose.y

        distance = math.sqrt(dist_x**2 + dist_y**2)
        target_theta = math.atan2(dist_y, dist_x)
        
        diff = target_theta - pose.theta
        if diff > math.pi:
            diff -= 2 * math.pi
        elif diff < -math.pi:
            diff += 2 * math.pi
        
        if distance > self.pose_threshold_linear:
            msg.angular.z = 4.0 * diff
            
            if abs(diff) > 0.1:
                msg.linear.x = 0.0
            else:
                msg.linear.x = 1.5 * distance
                if msg.linear.x > 3.0:
                    msg.linear.x = 3.0
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.call_catch_turtle_server(target.name)
            self.new_turtle_to_catch_ = None
            self.get_logger().info("Success")

        self.publisher_.publish(msg)
    def call_catch_turtle_server(self, turtle_name):
        client_ = self.create_client(CatchTurtle, "catch_turtle")
        while not client_.wait_for_service():
            self.get_logger().info("Waiting for service...")
        
        request = CatchTurtle.Request()
        request.name = turtle_name
        
        future = client_.call_async(request)
        future.add_done_callback(partial(self.callback_catch_turtle, turtle_name=turtle_name))

    def callback_catch_turtle(self, future, turtle_name):
        try:
            response = future.result()
            self.get_logger().info(f"Killed turtle {turtle_name}")
            
        except Exception as e:
            self.get_logger().info(f"Failed to kill turtle: {e}")


def main(args=None):
    rclpy.init(args=args)
    node = go_to_loc_node()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()

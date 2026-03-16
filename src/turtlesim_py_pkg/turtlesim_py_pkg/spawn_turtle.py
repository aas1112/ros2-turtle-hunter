#!/usr/bin/env python3
import math
import random
import rclpy
from rclpy.node import Node

from functools import partial
from turtlesim.srv import Spawn
from turtlesim.srv import Kill
from turtlesim_interfaces.msg import Turtle, TurtleArray
from turtlesim_interfaces.srv import CatchTurtle

class SpawnTurtleNode(Node):
    def __init__(self):
        super().__init__("spawn_turtle_node")
        self.name_ = "turtle"
        self.counter_ = 1
        self.new_turtles_ = []
        self.new_turtle_publisher_ = self.create_publisher(TurtleArray, "new_turtles", 10)
        self.catch_turtle_service_ = self.create_service(CatchTurtle, "catch_turtle", self.callback_catch_turtle)
        self.timer_ = self.create_timer(5.0, self.spawn_turtle)

    def callback_catch_turtle(self, request, response):
        self.call_kill_server(request.name)
        response.success = True
        return response

    def publish_new_turtles(self):
        msg = TurtleArray()
        msg.turtles = self.new_turtles_
        self.new_turtle_publisher_.publish(msg)
        
    
    def spawn_turtle(self):
        self.counter_ += 1
        x = random.uniform(0.0, 11.0)
        y = random.uniform(0.0, 11.0)
        theta = random.uniform(0.0, 2*math.pi)
        turtle_name = self.name_ + str(self.counter_)
        self.call_spawn_turtle_server(x, y, theta, turtle_name)


    def call_spawn_turtle_server(self, x, y, theta, turtle_name):
        client_ = self.create_client(Spawn, "/spawn")
        while not client_.wait_for_service():
            self.get_logger().info("Waiting for service...")
        
        request = Spawn.Request()
        request.x = x
        request.y = y
        request.theta = theta
        request.name = turtle_name
        
        future = client_.call_async(request)
        future.add_done_callback(partial(self.callback_spawn_turtle, x=x, y=y, theta=theta, turtle_name=turtle_name))

    def callback_spawn_turtle(self, future, x, y, theta, turtle_name):
        try:
            response = future.result()
            if response.name != "":
                self.get_logger().info(f"Spawned turtle {turtle_name} at ({x}, {y})")
                new_turtle = Turtle()
                new_turtle.x = x
                new_turtle.y = y
                new_turtle.theta = theta
                new_turtle.name = response.name
                self.new_turtles_.append(new_turtle)
                self.publish_new_turtles()
            else:
                self.get_logger().info(f"Failed to spawn turtle: {response.name}")
        except Exception as e:
            self.get_logger().info(f"Failed to spawn turtle: {e}")

    def call_kill_server(self, turtle_name):
        client_ = self.create_client(Kill, "/kill")
        while not client_.wait_for_service():
            self.get_logger().info("Waiting for service...")
        
        request = Kill.Request()
        request.name = turtle_name
        
        future = client_.call_async(request)
        future.add_done_callback(partial(self.callback_kill, turtle_name=turtle_name))

    def callback_kill(self, future, turtle_name):
        try:
            response = future.result()
            for (i, turtle) in enumerate(self.new_turtles_):
                if turtle.name == turtle_name:
                    self.new_turtles_.pop(i)
                    self.publish_new_turtles()
                    break
        except Exception as e:
            self.get_logger().info(f"Failed to kill turtle: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = SpawnTurtleNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
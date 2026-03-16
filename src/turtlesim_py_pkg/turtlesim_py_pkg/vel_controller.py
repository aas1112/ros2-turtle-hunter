#!/usr/bin/env python3
import sys
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class VelControllerNode(Node):
    def __init__(self):
        super().__init__("vel_controller_node")
        self.publisher_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.timer = self.create_timer(1, self.publisher_vel)

        self.get_logger().info("VelControllerNode has started")

    def publisher_vel(self):
        msg = Twist()
        # w =v/r
        linear_x = float(sys.argv[1])
        radius = float(sys.argv[2])
        msg.linear.x = linear_x
        msg.linear.y = 0.0
        msg.angular.z = float(linear_x / radius) # -3.14 --- +3.14 arasında değer alabilir
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = VelControllerNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()

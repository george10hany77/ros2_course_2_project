#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from pynput import keyboard

class keyboard_node(Node):
    def __init__(self):
        super().__init__("keyboard_controller_node")
        self.publisher = self.create_publisher(Twist, "/cmd_vel", 10)
        self.get_logger().info("the keyboard controller has started...")
        self.message_to_send = Twist()
        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        listener.start()

    def on_press(self, key):
        try:
            if key.char == 'w':
                self.message_to_send.linear.x = 0.5  # Move forward
            if key.char == 's':
                self.message_to_send.linear.x = -0.5  # Move backward
            if key.char == 'a':
                self.message_to_send.angular.z = 0.5  # Turn left
            if key.char == 'd':
                self.message_to_send.angular.z = -0.5  # Turn right
            if key.char == 'b':
                self.message_to_send.linear.x = 1.2 * self.message_to_send.linear.x
                self.message_to_send.linear.z = 1.2 * self.message_to_send.linear.z

            self.publisher.publish(self.message_to_send)
            self.get_logger().info(f"Published: {self.message_to_send}")
        except AttributeError:
            self.get_logger().warn("error while sending.. :(")

    def on_release(self, key):
        # Stop the robot when the key is released
        self.message_to_send.linear.x = 0.0
        self.message_to_send.angular.z = 0.0
        self.publisher.publish(self.message_to_send)
        self.get_logger().info("Stopped")

        if key == keyboard.Key.esc:
            # Stop listener
            return False

def main():
    rclpy.init()
    node = keyboard_node()
    rclpy.spin(node=node)
    rclpy.shutdown

if __name__ == "__main__":
    main()
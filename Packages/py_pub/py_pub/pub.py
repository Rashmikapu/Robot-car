import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState
from sensor_msgs.msg import Imu
from tf_transformations import euler_from_quaternion
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy


import sys
import select
import tty
import termios
# from pynput import keyboard

class Control_publisher(Node):

    def __init__(self):
        super().__init__('Control_publisher')
        
        self.joint_position_pub = self.create_publisher(Float64MultiArray, '/position_controller/commands', 1)
        self.wheel_velocities_pub = self.create_publisher(Float64MultiArray, '/velocity_controller/commands', 1)
        self.joint_state_pub = self.create_publisher(JointState, '/joint_states', 1)

        self.settings = termios.tcgetattr(sys.stdin)

        self.Kp = 0.01
        # self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        self.j = 0
        # Subscriber 
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )
        self.subscription = self.create_subscription(
            Imu,
            '/imu_plugin/out',
            self.listener_callback,
            qos_profile)
        self.subscription  # prevent unused variable warning

    def timer_callback(self):
        pass



    def listener_callback(self, msg):
        self.quat = [msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w]
        (_,_, yaw) = euler_from_quaternion(self.quat)
        self.pose_yaw = yaw
        # self.get_logger().info(f'I heard:  {self.pose_yaw}')
        positions = Float64MultiArray()
        velocities = Float64MultiArray()
        if self.pose_yaw < 0:
            steer_angle1 = (self.pose_yaw -(-3.14))*self.Kp
            steer_angle2 = (self.pose_yaw -(-3.14))*self.Kp
        else:
            steer_angle1 = (-3.14 + self.pose_yaw)*self.Kp
            steer_angle2 = (-3.14 + self.pose_yaw)*self.Kp
        linear_vel1 = 4.0
        linear_vel2 = 4.0    
        positions.data = [steer_angle1, steer_angle2]
        velocities.data = [linear_vel1, linear_vel2]
        self.joint_position_pub.publish(positions)
        self.wheel_velocities_pub.publish(velocities)

def main(args=None):
    rclpy.init(args=args)

    control_publisher = Control_publisher()

    rclpy.spin(control_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    control_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
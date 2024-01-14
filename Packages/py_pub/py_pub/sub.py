import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from sensor_msgs.msg import Imu
from tf_transformations import euler_from_quaternion
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

class IMUSub(Node):

    def __init__(self):
        super().__init__('IMUSub')
        
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


    def listener_callback(self, msg):
        self.quat = [msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w]
        (_,_, yaw) = euler_from_quaternion(self.quat)
        self.pose_yaw = yaw
        self.get_logger().info(f'Yaw : {self.pose_yaw}')


def main(args=None):
    rclpy.init(args=args)

    IMUsub = IMUSub()

    rclpy.spin(IMUsub)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    IMUsub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
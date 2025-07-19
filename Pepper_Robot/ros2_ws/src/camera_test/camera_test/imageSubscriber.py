#ROS2 packages
import rclpy
from rclpy.node import Node 
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
#OpenCv
import cv2

class ImageSubscriber(Node):

    def __init__(self):
        super().__init__('subscriber_node')

        self.bridgeObject = CvBridge()

        self.subscription = self.create_subscription(Image,"topic_camera_image",self.listener_callback,10)
        #prevent unused variable warning
        self.subscription

    def listener_callback(self, img_msg):
        self.get_logger().info('The image frame is received')

        img = self.bridgeObject.imgmsg_to_cv2(img_msg)

        cv2.imshow("Received image", img)
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    subscriber_node = ImageSubscriber()

    rclpy.spin(subscriber_node)
    
    rclpy.shutdown()
    
if __name__== "__main__":
    main()

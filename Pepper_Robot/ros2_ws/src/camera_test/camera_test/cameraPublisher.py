#ROS2 packages
import rclpy
from rclpy.node import Node 
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
#OpenCv
import cv2

class ImagePublisher(Node):
    _current_img_num = 0

    def __init__(self):
        super().__init__('publisher_node')
        cameraDeviceNumber = 0 #Number to indicate which camera in your system
        self.camera = cv2.VideoCapture(cameraDeviceNumber)

        self.bridgeObject = CvBridge()

        self.publisher = self.create_publisher(Image,"topic_camera_image", 10)
        
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.get_image_callback)

    def get_image_callback(self):
        #read image from the camera
        succes, frame = self.camera.read()
        #resize the image
        frame = cv2.resize(frame, (820, 640), interpolation=cv2.INTER_CUBIC)

        if succes:
            ros2_img_msg = self.bridgeObject.cv2_to_imgmsg(frame)
            #publish the image
            self.publisher.publish(ros2_img_msg)
        
        self.get_logger().info(f"Publishing image number {self._current_img_num}")
        self._current_img_num += 1

def main(args=None):
    rclpy.init(args=args)
    publisher_node = ImagePublisher()

    rclpy.spin(publisher_node)
    
    rclpy.shutdown()

if __name__== "__main__":
    main()

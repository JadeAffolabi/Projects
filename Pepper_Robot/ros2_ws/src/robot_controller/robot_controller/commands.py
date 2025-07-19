import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class Command_Node(Node):

    def __init__(self):
        super().__init__("robot_cmd")

        topic = "/model/vehicle_blue/cmd_vel"
        self.publisher =  self.create_publisher(Twist,topic, 10)

        timer_period = 0.5
        self.create_timer(timer_period, self.command_func)
    
    def command_func(self):
        #Keyboard commands
        option = input("Command [a, r, g, d] : ")
        #Create an instance of the message "speed"
        speed = Twist()
        if option == "a" :
            speed.linear.x = 1.0
        elif option == "r":
            speed.linear.x = -1.0
        elif option == "g":
            speed.angular.z = 1.0
            speed.linear.x = 1.0
        elif option == "d":
            speed.angular.z = -1.0
            speed.linear.x = 1.0

        #Publish the message
        self.publisher.publish(speed)

def main(args=None):
    rclpy.init(args=args)
    my_node = Command_Node()

    rclpy.spin(my_node)
    my_node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
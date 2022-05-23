#! /usr/bin/python3

# Python Imports
import cv2
import numpy as np

# ROS Imports
import rospy
from sensor_msgs.msg import Image
from rospy.numpy_msg import numpy_msg

    
class Face_Detection:
    def __init__(self):
        
        # path to haarcascade file (will need to chage on stretch)
        haar_file = '/home/lisa/face_detection_ws/src/face_detection_pkg/include/haarcascade_frontalface_default.xml'
        
        self.face_cascade = cv2.CascadeClassifier(haar_file)

        self.rgb_topic = rospy.get_param("rgbd_topic")
        self.roi_topic = rospy.get_param("roi_topic")
        
        # '0' is used for webcam
        # '6' is used for RGB camera on realsense (may change on stretch)
        # can find available cameras using "v4l2-ctl --list-devices" on cmd line
        self.webcam = cv2.VideoCapture(6)
        
        # subs to D435i just to run when the camera is working properly
        self.rgb_sub = rospy.Subscriber(self.rgb_topic, Image, self.get_roi, queue_size=100)
        self.roi_pub = rospy.Publisher(self.roi_topic, numpy_msg(np.int32), queue_size=10)
        

    def get_roi(self, data):
        (_, im) = self.webcam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 4)
        print(faces)
        faces = np.asarray(faces)
        if (faces != ()): # Need plan if no face is found
            print(type(faces[0][0]))
        self.roi_pub.publish(faces)
    
if __name__ == '__main__':
    try:
        rospy.init_node('Face_Detection', anonymous=True)
        processor = Face_Detection()
        rospy.spin()
    except rospy.ROSInterruptException:
        print('Face detection node failed!')
        pass
    cv2.destroyAllWindows()
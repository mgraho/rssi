#!/usr/bin/env python3


import bluetooth
import select
import rospy 
from std_msgs.msg import String
from rssi.msg import Num
import sys, signal

def callback(data):
    if (data.name=="rpi0" or data.name=="rpi1" or data.name=="rpi2"):
        name=data.name.replace("rpi", "")
        sender=data.sender.replace("rpi", "")
        rpix=int(name)
        senderID=int(sender)
        A[senderID][rpix]=data.rssi
    print("A=", A)
    
def listener():
    rospy.init_node('custom_listener', anonymous=True)
    rospy.Subscriber("device", Num, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
  
if __name__ == '__main__':
    A=[[0, 0, 0],[0, 0, 0],[0, 0, 0]]
    listener()


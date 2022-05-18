#!/usr/bin/env python3
import rospy
import bluetooth
import select
import rospy 
from std_msgs.msg import String
from rssi.msg import Num

class Rssi():
    def callback(self,data):
        self.pose=data
        if (data.name=="rpi0" or data.name=="rpi1" or data.name=="rpi2"):
            name=data.name.replace("rpi", "")
            sender=data.sender.replace("rpi", "")
            rpix=int(name)
            senderID=int(sender)
            self.A[senderID][rpix]=data.rssi
        print("A=", self.A)
    def __init__(self):
        self.A = [[0, 0, 0],[0, 0, 0],[0, 0, 0]]
        self.pub = rospy.Publisher("device",Num,queue_size=1)
        self.rate = rospy.Rate(10) #10 hz 
        self.device = Num()
        rospy.Subscriber("device",Num, self.callback)
	

    def run(self):
        while not rospy.is_shutdown():
            test=Num()
            test.name="rpi2"
            test.rssi=-70
            test.sender="rpi0"
            self.pub.publish(test)
            self.rate.sleep()
    

if __name__ == '__main__':
    rospy.init_node('pyclass')

    try:
        ne = Rssi()
        ne.run()
    except rospy.ROSInterruptException:pass


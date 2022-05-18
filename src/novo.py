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
            self.d = MyDiscoverer()
            self.d.find_devices(lookup_names = True)
            readfiles = [ self.d, ]
            while True:
                #vise uredaja
                rfds = select.select( readfiles, [], [] )[0]
                if self.d in rfds:
                    self.d.process_event()
                if self.d.done: break
            self.rate.sleep()
    
class MyDiscoverer(bluetooth.DeviceDiscoverer):

    def pre_inquiry(self):
        self.done = False

    def device_discovered(self, address, device_class, rssi, name):
        print("%s - %s" % (address, name))                              
        print("  RSSI: " + str(rssi))
        udaljenost=10**((-62-rssi)/(10*2))
        print("  udaljenost: " + str(udaljenost))
        device=Num()
        device.rssi=rssi
        device.address=address
        device.sender="rpix"
        device.name=name.decode('UTF-8')
       # pub.publish(device)
        
    def inquiry_complete(self):
        self.done = True
        
if __name__ == '__main__':
    rospy.init_node('pyclass')

    try:
        ne = Rssi()
        ne.run()
    except rospy.ROSInterruptException:pass


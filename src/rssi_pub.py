#!/usr/bin/env python3

import bluetooth
import select
import rospy 
from std_msgs.msg import String
from rssi.msg import Num
import sys, signal

def signal_handler(signal, frame):
    sys.exit(0)

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
        pub.publish(device)
        
    def inquiry_complete(self):
        self.done = True
        
        

if __name__ == "__main__":
    pub = rospy.Publisher('device',Num,queue_size=1)
    rospy.init_node('publisher')              
    try:
        while True:                           
            d = MyDiscoverer()
            d.find_devices(lookup_names = True)
            readfiles = [ d, ]
            signal.signal(signal.SIGINT, signal_handler)
            while True:
                #vise uredaja
                rfds = select.select( readfiles, [], [] )[0]
                if d in rfds:
                    d.process_event()
                if d.done: break
    except KeyboardInterrupt:
        print('interrupted!')

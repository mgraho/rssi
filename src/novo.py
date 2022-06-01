#!/usr/bin/env python3
import rospy
import bluetooth
import select
import rospy 
from std_msgs.msg import String
from rssi.msg import Num
import subprocess
import numpy

class Rssi():
    def callback(self,data):
        self.pose=data
        if data.name.find("rpi")!=-1:
           # if data.name.find("rpi0")!=-1:
           #     rpix=0
           # if data.name.find("rpi1")!=-1:
           #     rpix=1
           # if data.name.find("rpi2")!=-1:
           #     rpix=2
                #ime=data.name.replace("rpi", "")
                #name=ime.replace("\nhci0","")
            duljina=len(data.name)     
            for i in range(duljina):
                if data.name[i]=="r":
                    if data.name[i+1]=="p":
                        if data.name[i+2]=="i":
                            rpix=int(data.name[i+3])
            sender=data.sender.replace("rpi", "")
            #rpix=int(name)
            senderID=int(sender)
            self.A[senderID][rpix]=data.rssi
        print("A=", self.A)
        
        
    def __init__(self):
        n=3
        self.A = numpy.zeros((n,n))
        matrix = []
        for i in range(n):
            matrix.append([0] * n)
        print(matrix)
        print(self.A)
        self.rate = rospy.Rate(1) #1 hz 
        self.device = Num()
        #rospy.Subscriber("device",Num, self.callback)
        self.config = rospy.get_param('/consensus_params')
        self.name = rospy.get_namespace().strip('/')   
        print(self.name)
        self.index = int(self.config['mapping'].index(self.name))  
        #subprocess.run(['sudo','hciconfig','hciX','piscan'])
        pub = rospy.Publisher("device",Num,queue_size=1)
        # Create subscribers.
        for connected, to in zip(self.config['adjacency'][self.index], self.config['mapping']):
            if connected:
                rospy.Subscriber('/{}/device'.format(to), Num, self.callback, queue_size=3)
        
    def run(self):
        
        while not rospy.is_shutdown():

            result = subprocess.run(['sudo','btmgmt','find'], stdout=subprocess.PIPE)
            result=result.stdout.decode('UTF-8')
            #print(result)
            lista = result.split(" ")
            #print(lista)
            device=Num()
            length=len(lista)
            for i in range(length):
            
                if lista[i]=="rssi":
                    device.rssi=int(lista[i+1])
                            
                if lista[i]=="\nname":
                    device.name=lista[i+1] 
                    device.sender=self.name
                    
                    pub.publish(device)

            self.rate.sleep()
            
         
       
if __name__ == '__main__':
    rospy.init_node('pyclass')
    pub = rospy.Publisher("device",Num,queue_size=1)
    try:
        ne = Rssi()
        ne.run()
    except rospy.ROSInterruptException:pass


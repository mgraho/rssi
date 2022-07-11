#!/usr/bin/env python3
import rospy
import bluetooth
import select
import rospy 
from std_msgs.msg import String
from rssi.msg import Num
import subprocess
import numpy
from scipy.optimize import minimize
from scipy.signal import medfilt
from geometry_msgs.msg import Point
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PointStamped

class ListOfFive:
  def __init__(self):
    self.data = [[-63,-65,-87,-66,-64],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    print(self.data)
  def add(self,val):
    if len(self.data)==5:
      self.data=self.data[1:][1:]+[val]
    else:
      self.data+=[val]


  
  
  
if __name__ == '__main__':
    
    #matrica=numpy.zeros((n,5))
    matrica=[[-63,-65,-87,-66,-64],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    nizA=[-63,-75,-66,-87,-64]
    nizB=medfilt(nizA)
    print("Prije:  ", nizA)
   # print(nizB[5])
    print("Poslije:",nizB)
    print(round(sum(nizB)/len(nizB)))
    
    print(medfilt(matrica[0]))
    #matrica[0]=medfilt(matrica[0])
    print(matrica)
    rssi=-69
    for x in range(4):
        matrica[0][x]=matrica[0][x+1]
    matrica[0][4]=rssi
    print(matrica)
    n=2
    mjerenja=numpy.zeros((n,5))-62
    print(mjerenja)
    rpix=1
    print(nule)
    
    
    rospy.init_node('test')
    rate = rospy.Rate(1) 
    point=PointStamped()
    pose_msg=Pose()
    a=1
    pub = rospy.Publisher("mypoint",PointStamped,queue_size=1)
    pub2=rospy.Publisher("mypose",Pose,queue_size=1)
    while a==1:
       b=1 
       pose_msg.position.x=3
       pose_msg.position.y=1.5
       pose_msg.position.z=0
       pub2.publish(pose_msg)
       point.point.x=3
       point.point.y=3
       point.point.z=3
       pub.publish(point)
       
       rate.sleep()
   # l = ListOfFive()
   # for i in range(1,10):
    #    l.add(i)
    #print (l.data)

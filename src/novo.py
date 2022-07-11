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

class Rssi():
    def __init__(self):
        #n=3
        
        self.rate = rospy.Rate(1) #1 hz 
        self.device = Num()
        #rospy.Subscriber("device",Num, self.callback)
        self.config = rospy.get_param('/consensus_params')
        self.name = rospy.get_namespace().strip('/')   
        print(self.name)
        
        
        self.index = int(self.config['mapping'].index(self.name))  
        self.n=int(self.config['broj_uredaja'])
        self.mjerenja=numpy.zeros((self.n*self.n,5))-62
        self.A = numpy.zeros((self.n,self.n))
        self.X = numpy.zeros((self.n,2))
        matrix = []
        for i in range(self.n):
            matrix.append([0] * self.n)
        print(matrix)
        print(self.A)
        self.callback_number=0 
    
        subprocess.run(['sudo','hciconfig','hciX','piscan'])
        pub = rospy.Publisher("device",Num,queue_size=1)
        # Create subscribers.
        for connected, to in zip(self.config['adjacency'][self.index], self.config['mapping']):
            if connected:
                rospy.Subscriber('/{}/device'.format(to), Num, self.callback, queue_size=3)
                
                
    def callback(self,data):
        self.pose=data
        
        if data.name.find("rpi")!=-1:

            duljina=len(data.name)     
            for i in range(duljina):
                if data.name[i]=="r":
                    if data.name[i+1]=="p":
                        if data.name[i+2]=="i":
                            rpix=int(data.name[i+3])
            sender=data.sender.replace("rpi", "")
            
            senderID=int(sender)
            #rint(data.rssi)
            for x in range(4):
                self.mjerenja[senderID*self.n+rpix][x]=self.mjerenja[0][x+1]
                self.mjerenja[senderID*self.n+rpix][4]=data.rssi
            
            med=medfilt(self.mjerenja[senderID*self.n+rpix])
            rssi= round(sum(med)/len(med))
            udaljenost=10**((-62-rssi)/(10*2))
            temp=(udaljenost+self.A[senderID][rpix])/2
            self.A[senderID][rpix]=temp
            self.A[rpix][senderID]=temp
            self.callback_number=self.callback_number+1
            
            
        if self.callback_number>10:
            n = len(self.A)
            x0=numpy.zeros((1,n*2-3))
            bnds = ((0, None), (0, None))
            sol=minimize(self.objective,x0)
            est=sol.x
            X_est=[[0,0],[0,est[0]]]
            est=numpy.delete(est,0)
            X_est.append(numpy.reshape(est,(1,2)))
            print(X_est)
            #print(sol.fun)
        
        print("A=", self.A)
        
        
    def run(self):
        
        while not rospy.is_shutdown():
            print("skeniram")
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
                    print(device.rssi)
                if lista[i].find("name")!=-1:
                    device.name=lista[i+1] 
                    device.sender=self.name
                    if device.name.find("rpi")!=-1:
                        print(device.name)
                        pub.publish(device)

            self.rate.sleep()
            
    def objective(self,x):
        Y=self.A
        n = len(Y)
        X=[[0, 0] ,[0, x[0]]]
        x=numpy.delete(x,0)
        X.append(numpy.reshape(x,(1,2)))
        #print(X)
        mse = 0
        c = 0
        for i in range(n):
            for j in range(n):
                if (i != j):
                    d = numpy.linalg.norm(numpy.subtract(X[i], X[j]))
                    #print(d)
                    if Y[i][j] > 0:
                        
                        mse = mse + (d - float(Y[i][j]))** 2
                        c = c + 1
        mse = mse / c
        return mse
        
       
if __name__ == '__main__':
    rospy.init_node('pyclass')
    pub = rospy.Publisher("device",Num,queue_size=1)
    try:
        ne = Rssi()
        ne.run()
    except rospy.ROSInterruptException:pass


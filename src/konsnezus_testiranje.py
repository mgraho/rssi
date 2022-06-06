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



def objective(x):
        #Y=[[0,3,4],[3,0,5],[4,5,0]]
        Y=[[0,6,5],[6,0,5],[5,5,0]]
        n = len(Y)
        X=[[0, 0] ,[0, x[0]]]
        x=numpy.delete(x,0)
        X.append(numpy.reshape(x,(1,2)))
        #X = [[0, 0] ,[0, x[0]],[x[1], x[2]]]
        # print(X)
        mse = 0
        c = 0
        for i in range(n):
            for j in range(n):
                if (i != j):
                    d = numpy.linalg.norm(numpy.subtract(X[i], X[j]))
                    if Y[i][j] > 0:
                        
                        mse = mse + (d - float(Y[i][j]))** 2
                        c = c + 1
        mse = mse / c
        return mse
       
       
       
if __name__ == '__main__':
    Y=[[0,6,5],[6,0,5],[5,5,0]]  
    n=len(Y)  
    x0=numpy.zeros((1,n*2-3))
    #print (x0)
    bnds = ((0, None), (0, None))
   #sol=minimize(objective,x0,method='SLSQP',bounds=bnds)
    sol=minimize(objective,x0)
    print(sol.fun)
    print(sol.x)
    est=sol.x
    #X_est=[[0,0],[0,est[0]],[est[1],est[2]]]
    X_est=[[0,0],[0,est[0]]]
    est=numpy.delete(est,0)
    X_est.append(numpy.reshape(est,(1,2)))
    print(X_est)
    print(X_est[2])
    

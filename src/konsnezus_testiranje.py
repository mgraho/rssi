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



def objective(x,Y):
        n = size(Y, 1);
        X = [[0, 0] [0, x(1)]];
        X = [[X][ numpy.reshape(x,(2,end))]];


        mse = 0;
        c = 0;
        for i in range(n):
            for j in range(n):
                if (i != j):
                    d = norm(X[i,:] - X[j,:]);
                    if Y(i,j) > 0:
                        mse = mse + (d - Y(i, j))^ 2;
                        c = c + 1;

        mse = mse / c;

        return mse
       
       
       
if __name__ == '__main__':     
    matrica_za_testiranje=[[0,3,5][3,0,5][5,5,0]]
    x0=numpy.zeros((1,n*2-3))
    sol=minimize(objective(x,matrica_za_testiranje),x0)
    print(sol.fun)

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 13:09:50 2015

@author: bcolsen
"""

from __future__ import division, print_function
import numpy as np
import pylab as plt
import scipy.special as sp
import math

class PeirceCriteria:
    ''' use Peirce's Criterion to reject outlier data point from a dataset
        x - dataset to be evaluated (1xN vector)
        m - number of unknown quantities'''
    def __init__(self,x,m):
        # calculate mean and standard deviation
        x = np.array(x)
        
        xbar = np.mean(x)
        sigma = np.std(x, ddof=1)

        # Number of measurements
        N = len(x)

        # residuals
        delta = abs(x-xbar)

        # Number of rejected measurements
        Rej1 = 0

        n = 1 # number of suspect datapoints
        while(1):
            print( x, delta,sigma, m, )
            # no more data can be rejected
            if(N//2 <= n):
                print( 'no more datapoints can be rejected')
                break
            # compute R-value for current number of suspect datapoints
            R = self.PeirceBisect(N,n,m)
            print( delta <= sigma*R, sigma*R)
            # determine how many datapoints are rejected
            Rej2 = sum(delta > sigma*R)
            RejVec = delta > sigma*R
            AcceptVec = delta <= sigma*R
            
            # New dataset with removed datapoints
            
            x2 = x[delta <= sigma*R]
            #print x2
            
            # repeat process is number rejected datapoints increases, and increment
            # number oif suspect datapoints. Otherwise terminate rejection process 
            # if no additional points have been rejected. 
            if(Rej2 > Rej1):
                n += 1
                Rej1 = Rej2
            else:
                #n = n+1
                print('number reject datapoints not increasing')
                break
        try:
            self.x2 = x2
            self.RejVec = RejVec
            self.AcceptVec = AcceptVec
        except UnboundLocalError:
            self.x2 = x
            self.RejVec = [False]*len(x)
            self.AcceptVec = [True]*len(x)

    def PeirceFunc(self,N,n,m,x):
        ''' function to evalute in order to find roots for Peirce's criterion
            N - number of data samples
            n - number of data samples to be rejected
            m - number of independent variables (typically m=1)
            x - "R" value to be found, which is roots of function f'''
            
        #print m

        logQN = n*np.log(n) + (N-n)*np.log(N-n) - N*np.log(N)
        lamb = np.sqrt((N-m-n*x*x)/(N-m-n))

        f = (N-n)*np.log(lamb) + 0.5*n*(x*x-1) + n*np.log(sp.erfc(x/np.sqrt(2))) - logQN;
        return f
        
    def PeirceBisect(self,N,n,m):
        ''' bisection algorithm for determining "R" values of Peirce's criterion'''

        # precision epsilon
        eps = 2E-12

        # intitial guesses
        xl = 1
        xr = np.sqrt((N-m)/float(n)) - eps
        xo = (xl+xr)/2.0

        # check if a root exists
        if(self.PeirceFunc(N,n,m,xl)*self.PeirceFunc(N,n,m,xr) > 0 ):
            print( 'No root exists with R < 1, for N = %.0d, n = %.0d and m = %.0d'.format(N,n,m))
            
        # loop until root is found
        while(abs(self.PeirceFunc(N,n,m,xo)) > eps):
            if(self.PeirceFunc(N,n,m,xl)*self.PeirceFunc(N,n,m,xo) < 0):
                xr = xo
                xo = (xl+xr)/2.0
            else:
                xl = xo
                xo = (xl+xr)/2.0
                
             #disp((PeirceFunc(N,n,m,xo)))
        R = xo
        return R
        
if __name__ == "__main__":
    m = 1
    x = [4.24,3.94,3.85,3.82,3.60]
    #x = [101.2, 90.0, 99.0, 102.0, 103.0, 100.2, 89.0, 98.1, 101.5, 102.0]
    test1_PC = PeirceCriteria(x,m)
    r = test1_PC.PeirceBisect(5,2,1)  #1.200
    print( test1_PC.x2, test1_PC.RejVec, r)



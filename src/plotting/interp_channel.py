'''
An class to interpolate the buoyancy field in the SO along lines
with constant slope - only to mke fancy looking plots
'''

import numpy as np
from scipy.optimize import brenth

class Interpolate_channel(object):
    def __init__(
            self,            
            y=None,          # y-grid
            z=None,          # z-grid
            bs=None,         # surface buoyancy
            bn=None,         # buoyancy profile in the north
    ):
 
        # initialize grid:
        if isinstance(y,np.ndarray):
            self.y = y
        else:
            raise TypeError('y needs to be numpy array providing grid levels') 
        if isinstance(z,np.ndarray):
            self.z = z
        else:
            raise TypeError('z needs to be numpy array providing grid levels') 
        
        self.bs=self.make_func(bs,'bs',self.y)
        self.bn=self.make_func(bn,'bn',self.z)
             
        
    def make_func(self,myst,name,xin):
    # turn array or float into callable function (if needed)    
        if callable(myst):
            return myst
        elif isinstance(myst,np.ndarray):
            def funfun(x): return np.interp(x,xin,myst)
            return funfun
        elif isinstance(myst,float):
            def funfun(x): return myst +0*x
            return funfun
        else:
            raise TypeError(name,'needs to be either function, numpy array, or float') 
           
          
    def __call__(self, y, z):
        l=self.y[-1]
        if z == 0.0 and y == l:
            # slope ill defined at (l,0); evaluate infinitesimally below the surface:
            z = -1e-10  
        def f2(x):
               # function to help determine slope at bottom of vent. region
               return self.bn(x)-self.bs(0)            
        def f(x):
               # function to help determine slope in vent. region
               return self.bn(z-x*(l-y))-self.bs(y+z/x)            
        # first determine slope at bottom of vent. region here
        sbot=-brenth(f2, self.z[0],0.)/l
        # than set slope for stuff above and below...           
        if -z>sbot*y:
          s=sbot
        else:
          s=brenth(f, 1.e-12,1.0)
        return self.bn(z-s*(l-y))
    
    def gridit(self):
        ny=len(self.y)
        nz=len(self.z)
        barray=np.zeros((ny,nz))
        for iy in range(0,ny):
            for iz in range(0,nz):
               barray[iy,iz]=self(self.y[iy],self.z[iz])
        return barray
      
    
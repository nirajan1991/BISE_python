# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 13:52:20 2021

@author: Nirajan
"""
#%%
'''
This script emulates BISE function written in R
https://rdrr.io/github/ozjimbob/ecbtools/src/R/bise.r
'''
#%%
import numpy as np

def BISE(x, slide_period = 20, slope_threshold = 0.2):
    slope_threshold_value = 0
    days = len(x)
    x = np.concatenate((x,x,x)).flatten()
    cor_x = np.zeros((len(x),1))
    
    for i in range (2,3*days):
        if x[i] >= x[i-1]:
            cor_x[i] = x[i]
        else:
            if (i+slide_period) > 3*days-1:
                period = 3*days - i -1
            else:
                period = slide_period
            
            slope_threshold_value = x[i] +slope_threshold * (x[i-1] - x[i])
            bypassed_elems = 0
            ndvi_chosen = 0
            
            for j in range(i+1, i+period-1):
                if (x[j] > slope_threshold_value) and (x[j] > ndvi_chosen):
                    ndvi_chosen = x[j]
                    bypassed_elems = j-i
                
                if ndvi_chosen >= x[i-1]:
                    break
                
            if ndvi_chosen == 0:
                cor_x[i] = x[i]
            else:
                for j in range(0, bypassed_elems):
                    cor_x[i-1+j] = -1
                i = i + bypassed_elems
                cor_x[i] = ndvi_chosen
        
    cor_x = cor_x [days:days*2]
    
    #i excluded the last part because it will replace all the -1 with the previous values
        
    return cor_x
#%%
#test the use of BISE on mock data
xx = np.array([0.2, 0.3, 0.4, 0.5, 0.8, 0.2, 0.7, 0.65, 0.6, 0.5, 0.4, 0.38, 0.2])
corr_xx = BISE(xx, slide_period = 5, slope_threshold = 0.2)
#%%
'''
Instruction for editing the script from github
Keep this file in the same folder as your main script
line 42 to 46
import BISE
#apply the bise algorithm
bisendvi = BISE.BISE(ndvi, byref(slidingperiod))
bisendvi[bisendvi == -1] = np.nan
'''
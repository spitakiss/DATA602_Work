#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
created on Sun Mar 26 16:27:20 2017
@author: aarong

Program to time functions related to
curve fitting using both base Python
and SciPy.  This program also provides parameter
estimates for the various fitted models

"""

# import modules
import csv
import timeit as ti
import urllib2
import numpy as np
from scipy.optimize import curve_fit

# read csv
def scrub_csv(url):
    """
    function takes url for csv file, removes header row,
    converts numeric columns to floats,
    and returns rows in list form
    """
    rows = []
    f = urllib2.urlopen(url)
    reader = csv.reader(f)
    
    # read each row in file, remove header line
    for row in reader:
        if reader.line_num ==1:
            continue
        
        # convert each cell to float, if possible
        temprow = row
        for i in range(len(temprow)):
            try:
                temprow[i] = float(temprow[i])
            except:
                pass
        
        # append scrubbed row to master list
        rows.append(temprow)
               
    f.close()
    return rows


# fit ols using base python
def ols_est(data,xcol,ycol):
    """
    function takes list input, and specified column numbers
    for x and y variable, respectively.
    outputs slope and intercept estimates
    """
    sumprodxy = 0
    sumx = 0
    sumy = 0  
    sumx2 = 0 
    n = len(data)
    
    for row in data:
        sumprodxy += row[xcol]*row[ycol]
        sumx += row[xcol]
        sumy += row[ycol]
        sumx2 += row[xcol]**2
    
    # slope estimate
    b = (n * sumprodxy - sumx * sumy) / (n*sumx2 - (sumx)**2)

    # intercept estimate
    a = (sumy - b*sumx)/n       
    
    # return intercept and slope, respectively
    return (a,b)

# fit to curve using scipy
def scipy_fit(func, data, xcol_name,ycol_name):
    """
    function takes numpy array input and specified column names
    for x and y variable, respectively.
    outputs paramater estimates for
    specified model using scipy curve_fit()
    """
      
    # fit linear model using curve_fit
    popt, pcov = curve_fit(func,data[xcol_name],data[ycol_name])
    
    # return model paramter estimates
    return popt

 
def line(x,a,b):
    """
    helper function for scipy_fit
    defines linear model
    """
    return b*x + a

def poly2(x,a,b,c):
    """
    helper function for scipy_fit
    defines polynomial order 2 model
    """
    return c*x**2 + b*x + a
    


if __name__ == "__main__":
    
    
    # url with data
    url = 'https://raw.githubusercontent.com/spitakiss/DATA602_Work/master/Homework7/brainandbody.csv'
    
    # save data as standard list of list for base ols function
    myfile = scrub_csv(url)

    # store data as numpy array for scipy based functions 
    np_myfile = np.genfromtxt(url, delimiter=",", skip_header=1,dtype=[('f0','S25'),('f1','<f8'),('f2','<f8')])
        
    # iterations for timer function
    n = 10000
    
    
    ####### test ols using base python####################################################
    print "OLS BASE TEST".center(70,'=')
    
    #timer
    t = ti.Timer('ols_est(myfile,1,2)','from __main__ import ols_est, myfile') 
    print "%s timer using %s: %d loops = %f seconds" % ("OLS", "base python", n, t.timeit(n))
    
    # parameter estimates
    base_ols = ols_est(myfile,1,2)
    print "intercept estimate %f:\nslope estimate: %f" % (base_ols[0],base_ols[1])
    
    ####### test ols using scipy and curve_fit()####################################################
    print "OLS SCIPY TEST".center(70,'=')
    
    #timer
    t = ti.Timer('scipy_fit(line,np_myfile,"f1","f2")','from __main__ import scipy_fit,line,np_myfile') 
    print "%s timer using %s: %d loops = %f seconds" % ("OLS", "sci py", n, t.timeit(n))
    
    # parameter estimates
    sp_ols = scipy_fit(line, np_myfile,'f1','f2')
    print "intercept estimate %f:\nslope estimate: %f" % (sp_ols[0],sp_ols[1])
    
    ####### test polynomial fit (order2) using scipy and curve_fit()####################################################
    print "POLY2 SCIPY TEST".center(70,'=')
    
    #timer
    t = ti.Timer('scipy_fit(poly2,np_myfile,"f1","f2")','from __main__ import scipy_fit,poly2,np_myfile') 
    print "%s timer using %s: %d loops = %f seconds" % ("Polynomial order 2", "sci py", n, t.timeit(n))
    
    # parameter estimates
    sp_poly = scipy_fit(poly2,np_myfile,"f1","f2")
    print "intercept estimate %f:\ncoefficient of linear term: %f\ncoefficient of quadratic term: %f" % (sp_poly[0],sp_poly[1],sp_poly[2])

 
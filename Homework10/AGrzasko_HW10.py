#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 09:54:10 2017

@author: aarong

Assignment:
    1. Express the cars.data.csv data as a series of bar graphs. 
       x-axis = feature; y-axis=count; cols = buying, maint, safety, doors 
    2. Plot brainandbody.csv data in scatter plot.  Add regression line plot.  
       Annotate with OLS equation 
    3. Overlay centers of mass point on objects.png image
    4. Plot line graph of server requests by hour using epa-http.txt
"""

# import modules
import pandas as pd
import numpy as np
import scipy.misc as misc
import scipy.ndimage as ndimage
import matplotlib.pyplot as plot
import urllib2


##### 1. Bar Plots of cars.data.csv###################################################################### 

# read in data
car_url = 'https://raw.githubusercontent.com/spitakiss/DATA602_Work/master/Homework3/cars.data.csv'
car_cols = ['buying','maint','doors','persons','lugboot','safety','carclass'] 
car_data = pd.read_csv(car_url, names=car_cols, header=None)

# define relevant columns (keys) from car_data, and establish proper ordering for category values 
cats = {'buying': ['low','med','high','vhigh'],'maint':['low','med','high','vhigh'],\
          'safety':['low','med','high'],'doors': ['2','3','4','5more'] }

# starting index value for sub plots.  
sp_num = 221

# use loop to make bar plots for each of four car attributes
for k,v in cats.items():
    plot.subplot(sp_num)
    y = car_data[k].value_counts().reindex(v)
    x = range(len(y))
    plot.bar(x,y,width=1.0, edgecolor='white')
    plot.xticks(x,y.index)
    plot.ylabel('counts')
    plot.xlabel('category')
    plot.title(k)
    plot.tight_layout()
    sp_num += 1
    plot.grid(True)

plot.show()

##### 2. OLS Plot of brainandbody.csv ######################################################################

# read in data
brain_url = 'https://raw.githubusercontent.com/spitakiss/DATA602_Work/master/Homework7/brainandbody.csv'
brain_data = pd.read_csv(brain_url)
brain_data.columns.values[0]='animal'

# establish x and y coords                         
x = brain_data["body"]
y = brain_data["brain"]

# set up initial scatter plot with raw data points
plot.scatter(x,y, color="green")
plot.ylabel('brain weight')
plot.xlabel('body weight')
plot.title('OLS: Brain Weight Regressed on Body Weight')

# fit and plot regression line
m,b  = np.polyfit(x,y,1)
plot.plot(x, m*x +b, "-", color="black")

# annotate plot with ols equation
ols_eqn = "y = "+str(round(m,3))+"x + "+str(round(b,3))
plot.annotate(ols_eqn, xy=(3000,6000))

plot.show()

##### 3. Centers of Mass Plot of objects.png ################################################################## 


# scripts below are an abbreviated (non-function) version of my HW 8 submission to determine center of mass 

# read image
img_url = 'https://raw.githubusercontent.com/spitakiss/DATA602_Work/master/Homework8/images/objects.png'
obj_img = misc.imread(urllib2.urlopen(img_url))

# filter image
gf = ndimage.gaussian_filter(obj_img,2)
filter_obj = gf > gf.mean()

# determine center of mass for each object
com =[]
for i in range(1, ndimage.label(filter_obj)[1]+1):
    com.append(ndimage.measurements.center_of_mass(filter_obj, ndimage.label(filter_obj)[0],i)[0:2])

# change center of mass (y,x) format to (x,y)
com = [(i[1],i[0]) for i in com]

# plot raw image and centers of mass
plot.imshow(obj_img)
plot.scatter(*zip(*com))
plot.title('Plot of Centers of Mass')
plot.xlabel('x val')
plot.ylabel('y val')
plot.show()


##### 4. Line Plot Reqs by Hour using epa-http.txt ##################################################################  

# read data
epa_url = 'https://raw.githubusercontent.com/spitakiss/DATA602_Work/master/Homework9/epa-http.txt'
epa_cols = ['host','datetime','request','reply_cd','bytes']
epa_data = pd.read_csv(epa_url, sep='\s+', escapechar='=', header=None, names=epa_cols, na_values = "-")

# create hour field
epa_data['hour'] = epa_data['datetime'].str.extract(r'(?<=\d\d:)(\d\d)',expand=True)

# group by hour, count of items in "request" field (defining this quantity as number of requests)
hour_req = epa_data.groupby('hour').count()['request'] 

# helper function to convert military time to standard time
def mil_to_std(mil_hr):
    return str(mil_hr % 12 + (12 if mil_hr in (0,12,24) else 0)) + ('p' if (mil_hr > 11 and mil_hr < 24)  else 'a')

# format x axis in plot
x = range(24)
xlab = [str(mil_to_std(i))+"-"+str(mil_to_std(i+1)) for i in range(24)] # x axis labels in standard time
plot.plot(x,hour_req)
plot.xticks(x,xlab, rotation='vertical')

# additional plot formatting 
plot.title("Number of EPA Server Requests by Hour")
plot.xlabel("hour")
plot.ylabel("no. requests")
plot.show()


"""
References: 
1. Plotting regression line: http://stackoverflow.com/questions/6148207/linear-regression-with-matplotlib-numpy  
2. Plotting list of tuples and zip function: http://stackoverflow.com/questions/18458734/python-plot-list-of-tuples
3. General matplotlib help: http://matplotlib.org/users/pyplot_tutorial.html
4. More general matplotlib help: http://www.labri.fr/perso/nrougier/teaching/matplotlib/simple-plot
"""

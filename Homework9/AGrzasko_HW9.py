#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 08:57:19 2017
@author: aarong

File Field Definitions:
    1. host name/address 
    2. day/time of request
    3. http request
    4. http reply code
    5. bytes in reply

Assignment Questions:
    1. Which hostname or IP address made the most requests?
    2. Which hostname or IP address received the most total bytes from the server?  How many bytes did it receive? 
    3. During what hour was the server the busiest in terms of requests?
    4. Which .gif image was downloaded the most during the day?
    5. What HTTP reply codes were sent other than 200?
    
"""

# import modules
import pandas as pd
import urllib2

# read text file 
def read_epa(url):
    """
    read, scrub epa text file.
    """
    f = urllib2.urlopen(url)
    colnames = ['host','datetime','request','reply_cd','bytes']
    my_df = pd.read_csv(f, sep='\s+', escapechar='=', header=None, names=colnames, na_values = "-")
    f.close()
    return my_df


# helper function to convert military time hour to standard time
def mil_to_std(mil_hr):
    """
    helper function to convert military time to standard time
    """
    return str(mil_hr % 12 + (12 if mil_hr == 12 else 0)) + ('pm' if mil_hr > 11 else 'am')


if __name__ == "__main__":
    
    # read in data
    df = read_epa('https://raw.githubusercontent.com/spitakiss/DATA602_Work/master/Homework9/epa-http.txt')
    
    # 1. Top hostname in terms of number of requests 
    hostreq = df.groupby('host').count()['request'] # group by host and summarize by number of counts       
    maxreq_host = hostreq.argmax()                  # top host in terms of number of requests
    maxreq = hostreq[maxreq_host]                   # total requests for top host                  
    
    print "1. The top requester was %s with %d requests.\n" % (maxreq_host, maxreq)
    
    # 2. Top hostname in terms of of number of bytes received from server
    hostbytes = df.groupby('host').sum()['bytes']   # group by host, sum total number of bytes
    maxbytes_host = hostbytes.argmax()              # host with highest numbers of bytes
    maxbytes = hostbytes[maxbytes_host]             # highest number of bytes received over course of 24 hours
    
    print "2. The top host in terms of byte consumption was %s with %d bytes received.\n" % (maxbytes_host, round(maxbytes,0))
    
    # 3. Busiest hour ranked by number of requests--assuming ok to aggregate 23:00 hour from both calendar days
    df['hour'] = df['datetime'].str.extract(r'(?<=\d\d:)(\d\d)',expand=True) # create new df column, "hour", in string format, len = 2
    hour_req = df.groupby('hour').count()['request'] # group by hour, count number of requests                                                                                                             
    maxreq_hour = int(hour_req.argmax())             # busiest hour
    maxreq_num = hour_req[hour_req.argmax()]         # number of requests during busiest hour 
    
    print "3. The busiest hour was between %s and %s with %d total requests.\n" % (mil_to_std(maxreq_hour), mil_to_std(maxreq_hour + 1), maxreq_num)
    
    # 4. Most popular gif image
    df['gif_image'] = df['request'].str.extract(r'([\w-]+\.gif)',expand=True)   # add new column, "gif_image
    img_ct = df.groupby('gif_image').count()['request'] # group by gif_image, count number of requests
    max_img = img_ct.argmax()                           # most requested image
    max_img_ct = img_ct[max_img]                        # number of requests for most popular image
    
    print "4. The most popular gif image was %s with %d total requests.\n" %(max_img, max_img_ct) 
    
    # 5. non 200 reply codes
    reply_cd_excl200 =  df[df['reply_cd'] != 200]['reply_cd'].unique() # unique, non 200 reply codes
  
    print "5. The unique reply codes--excluding code 200--were: %r.\n" % sorted(list(reply_cd_excl200))
                          
    
    
    
    

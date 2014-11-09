#!/usr/bin/python
import os,re
import urllib
import sys
import json
import requests

CLOUDFARE_EMAIL="you@example.com"	#Email you use to login to CloudFlare
CLOUDFARE_API_KEY="put key here"        #CloudFlare API key	
BASE_DOMAIN='example.com'	        #Domain Name whose records are being modified 
RECORD_TYPE='A'   	                #See "Type" Column on https://www.cloudflare.com/dns-settings?z=example.com
RECORD_NAME='@'	                        #See "Name" Column on https://www.cloudflare.com/dns-settings?z=example.com


def get_real_ip():
    url ='http://ip.jsontest.com/'
    resp = requests.get(url=url)
    data = json.loads(resp.text)
    ip   = data[u'ip']
    return ip

def getCFRecordNum():

    url ='https://www.cloudflare.com/api_json.html'

    params = dict(
        a     =   'rec_load_all',
        tkn   =   CLOUDFARE_API_KEY,
        email =   CLOUDFARE_EMAIL,
        z     =   BASE_DOMAIN
        )
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    data = data[ u'response']
    data = data[ u'recs']
    data = data[ u'objs']
    data = data[ 0]
    rec_id = data[u'rec_id']
 
    return rec_id

def update_cf(saved_ip):
    rec_id = getCFRecordNum()
    url ='https://www.cloudflare.com/api_json.html'
    params = dict(
        a            = 'rec_edit',
        tkn          = CLOUDFARE_API_KEY,
        id           = rec_id,
        email        = CLOUDFARE_EMAIL,
        z            = BASE_DOMAIN,
        type         = RECORD_TYPE,
        name         = RECORD_NAME,
        content      = saved_ip,
        service_mode = '1',
        ttl          = '1'
        )
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    status = data[ u'result']

    data = data[u'request']
    current_ip = data[u'content']
    print "Update:",status
    print "New IP in A Record:",current_ip
    print "New Device IP Address:",saved_ip
 
#Store IP on Server

if os.path.isfile('ip.txt'):
    file = open('ip.txt','r')
    saved_ip =file.read( )
    file.close()
    device_ip = get_real_ip()
  
else:
   print 'could not locate saved IP. updating now.....'
   file = open('ip.txt','w')
   device_ip = get_real_ip()
   file.write(device_ip)
   file.close()
   file = open('ip.txt','r')
   saved_ip =file.read( )
   file.close()
   update_cf(saved_ip)

if saved_ip !=  device_ip: 
    print 'IP has changed. updating now....'
    update_cf(device_ip)
  
    file = open('ip.txt','w')
    file.write(device_ip)
    file.close()
    file = open('ip.txt','r')
    saved_ip =file.read( )
    file.close()
    device_ip = get_real_ip()

else:
   print "All Cool....."

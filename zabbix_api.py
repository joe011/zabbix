#!/usr/bin/python 
#coding:utf-8 
 
import json 
import urllib2 
from urllib2 import URLError 
import sys 
 
class zabbix_api: 
	def __init__(self): 
	    self.url = 'http://localhost/api_jsonrpc.php' 
	    self.header = {"Content-Type":"application/json"}         
	     
	     
	def user_login(self): 
	    data = json.dumps({ 
	                       "jsonrpc": "2.0", 
	                       "method": "user.login", 
	                       "params": { 
	                                  "user": "Admin", 
	                                  "password": "zabbix" 
	                                  }, 
	                       "id": 0 
	                       }) 
	     
	    request = urllib2.Request(self.url, data) 
	    for key in self.header: 
	        request.add_header(key, self.header[key]) 
	 
	    try: 
	        result = urllib2.urlopen(request) 
	    except URLError as e: 
	        print "Auth Failed, please Check your name and password:", e.code 
	    else: 
	        response = json.loads(result.read()) 
	        result.close() 
	        #print response['result'] 
	        self.authID = response['result'] 
	        return self.authID 
	     
	def host_get(self,hostName=''): 
	    data=json.dumps({
	            "jsonrpc": "2.0",
	            "method": "host.get",
	            "params": {
	                      "output": "extend",
	                      "filter":{"host":hostName} 
	                      },
	            "auth": self.user_login(),
	            "id": 1
	            })
	    request = urllib2.Request(self.url,data) 
	    for key in self.header: 
	        request.add_header(key, self.header[key]) 
	         
	 
	    try: 
	        result = urllib2.urlopen(request) 
	    except URLError as e: 
	        if hasattr(e, 'reason'): 
	            print 'We failed to reach a server.' 
	            print 'Reason: ', e.reason 
	        elif hasattr(e, 'code'): 
	            print 'The server could not fulfill the request.' 
	            print 'Error code: ', e.code 
	    else: 
	        response = json.loads(result.read()) 
	        #print response
	        result.close() 
	        print "Number Of Hosts: \033[31m%s\033[0m"%(len(response['result']))
	        for host in response['result']:      
	            	status={"0":"OK","1":"Disabled"}
			available={"0":"Unknown","1":"available","2":"Unavailable"}
			#print host
			if len(hostName)==0:
                		print "HostID : %s\t HostName : %s\t Status :\033[32m%s\033[0m \t Available :\033[31m%s\033[0m"%(host['hostid'],host['name'],status[host['status']],available[host['available']])
			else:
                		print "HostID : %s\t HostName : %s\t Status :\033[32m%s\033[0m \t Available :\033[31m%s\033[0m"%(host['hostid'],host['name'],status[host['status']],available[host['available']])
				return host['hostid']

	def hostgroup_get(self, hostgroupName=''): 
	    data = json.dumps({ 
	                       "jsonrpc":"2.0", 
	                       "method":"hostgroup.get", 
	                       "params":{ 
	                                 "output": "extend", 
	                                 "filter": { 
	                                            "name": hostgroupName 
	                                            } 
	                                 }, 
	                       "auth":self.user_login(), 
	                       "id":1, 
	                       }) 
	     
	    request = urllib2.Request(self.url,data) 
	    for key in self.header: 
	        request.add_header(key, self.header[key]) 
	          
	    try: 
	        result = urllib2.urlopen(request) 
	    except URLError as e: 
	        print "Error as ", e 
	    else: 
	        #print result.read()
	        response = json.loads(result.read()) 
	        result.close() 
	        #print response()
	        for group in response['result']:
	        	if  len(hostgroupName)==0:
	          		print "hostgroup: %s\tgroupid : %s" %(group['name'],group['groupid'])
			else:
	          		print "hostgroup: %s\tgroupid : %s" %(group['name'],group['groupid'])
	           		self.hostgroupID = group['groupid'] 
	           		return group['groupid'] 


	def template_get(self,templateName=''): 
	    data = json.dumps({ 
	                       "jsonrpc":"2.0", 
	                       "method": "template.get", 
	                       "params": { 
	                                  "output": "extend", 
	                                  "filter": { 
	                                             "name":templateName                                                        
	                                             } 
	                                  }, 
	                       "auth":self.user_login(), 
	                       "id":1, 
	                       })
	     
	    request = urllib2.Request(self.url, data) 
	    for key in self.header: 
	        request.add_header(key, self.header[key]) 
	          
	    try: 
	        result = urllib2.urlopen(request) 
	    except URLError as e: 
	        print "Error as ", e 
	    else: 
	        response = json.loads(result.read()) 
	        result.close() 
	        #print response
	        for template in response['result']:                
	            if len(templateName)==0:
	                print "template :%s\t  id : %s" % (template['name'], template['templateid'])
	            else:
	                self.templateID = response['result'][0]['templateid'] 
	                return response['result'][0]['templateid']
	def hostgroup_create(self,hostgroupName):

	    if self.hostgroup_get(hostgroupName):
	        print "hostgroup %s is exist !"%hostgroupName
	        sys.exit(1)
	    data = json.dumps({
	                      "jsonrpc": "2.0",
	                      "method": "hostgroup.create",
	                      "params": {
	                      "name": hostgroupName
	                      },
	                      "auth": self.user_login(),
	                      "id": 1
	                      })
	    request=urllib2.Request(self.url,data)

	    for key in self.header: 
	        request.add_header(key, self.header[key]) 
	          
	    try: 
	        result = urllib2.urlopen(request)
	    except URLError as e: 
	        print "Error as ", e 
	    else: 
	        response = json.loads(result.read()) 
	        result.close()
	        print "hostgroupID : %s"%response['result']['groupids']


	             
	def host_create(self, hostip, hostgroupName, templateName): 
	    group_list=[]
	    template_list=[]
	    for i in hostgroupName.split(','):
	        var = {}
	        var['groupid'] = self.hostgroup_get(i)
	        group_list.append(var)
	    for i in templateName.split(','):
	        var={}
	        var['templateid']=self.template_get(i)
	        template_list.append(var)	

	    print group_list
	    print template_list
	    data = json.dumps({ 
	                       "jsonrpc":"2.0", 
	                       "method":"host.create", 
	                       "params":{ 
	                                 "host": hostip, 
	                                 "interfaces": [ 
	                                                    { 
	                                                        "type": 1, 
	                                                        "main": 1, 
	                                                        "useip": 1, 
	                                                        "ip": hostip, 
	                                                        "dns": "", 
	                                                        "port": "10050" 
	                                                    } 
	                                                ], 
	                              #  "groups": [ { "groupid": self.hostgroup_get(hostgroupName)} ], 
	                               # "templates": [  { "templateid": self.template_get(templateName) }], 
	                               "groups": group_list,
	                               "templates": template_list,
	                                 }, 
	                       "auth": self.user_login(), 
	                       "id":1                   
	    }) 
	    request = urllib2.Request(self.url, data) 
	    for key in self.header: 
	        request.add_header(key, self.header[key]) 
	          
	    try: 
	        result = urllib2.urlopen(request) 
	    except URLError as e: 
	        print "Error as ", e 
	    else: 
	        response = json.loads(result.read()) 
	        result.close() 
	        print "host : %s \tid : %s" % (hostip, response['result']['hostids']) 
	        self.hostid = response['result']['hostids'] 
	        return response['result']['hostids'] 


	def host_disable(self,hostip):
		data=json.dumps({
		"jsonrpc": "2.0",
		"method": "host.update",
		"params": {
		"hostid": self.host_get(hostip),
		"status": 1
		},
		"auth": self.user_login(),
		"id": 1
		})
		request = urllib2.Request(self.url,data)
	    	for key in self.header:
	        	request.add_header(key, self.header[key]) 		
	    	try: 
	        	result = urllib2.urlopen(request)
	    	except URLError as e: 
	        	print "Error as ", e 
	    	else: 
	        	response = json.loads(result.read()) 
	        	result.close()
	        	print '----主机现在状态------------'
			print self.host_get(hostip)
	             
	             
if __name__ == "__main__": 
	pass
	#example
	#zabbix=zabbix_api()
	#print zabbix.host_get()
	#print zabbix.host_get('192.168.2.21')
	#print zabbix.hostgroup_get('test02')
	#print zabbix.template_get()
	#print zabbix.template_get('Template OS Linux')
	#print zabbix.hostgroup_get('Linux servers')
	#a=zabbix.hostgroup_create('test02')
	#print a
	
	#zabbix.host_create('192.168.2.20', 'Linux servers,test01 ', 'Template OS Linux,Template App MySQL')
	#zabbix.host_create('192.168.2.18', 'test02', 'Template OS Linux')
	#print zabbix.host_disable('192.168.2.18')

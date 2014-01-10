#!/usr/bin/python
zabbix=zabbix_api()
#获取所有主机列表
 zabbix.host_get()
#查询单个主机列表
 zabbix.host_get('192.168.2.1')
#获取所有主机组列表
 zabbix.hostgroup_get()
#查询单个主机组列表
 zabbix.hostgroup_get('test01')
#获取所有模板列表
 zabbix.template_get()
#查询单个模板信息
 zabbix.template_get('Template OS Linux')
#添加一个模板
zabbix.hostgroup_create('test01')
#添加一个主机，支持将主机添加进多个组，多个模板，多个组、模板之间用逗号隔开，如果添加的组不存在，新创建组
zabbix.host_create('192.168.2.1', 'test01', 'Template OS Linux')
zabbix.host_create('192.168.2.1', 'Linux servers,test01 ', 'Template OS Linux,Template App MySQL')
#禁用一个主机
 zabbix.host_disable('192.168.2.1')
#删除host,支持删除多个，之间用逗号
zabbix.host_delete('192.168.2.1,192.168.2.2')

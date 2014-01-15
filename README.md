zabbix
======

###简介：
		根据日常工作中常用到zabbix的功能，整理以下功能
		1.基于 zabbix 官方 api
		2.提供查询单个或者多个host、hostgroup、template功能
		3.提供增加host,hostgroup功能
		4.提供disable host功能
		5.添加删除host功能
###使用说明：
		修改自己的url，及user,password,详见example.py

###帮助信息
		直接执行 python zabbix_api.py
		usage: zabbix_api.py [options]

		zabbix api
		
		optional arguments:
		  -h, --help            show this help message and exit
		  -H [LISTHOST], --host [LISTHOST]
		                        查询主机
		  -G [LISTGROUP], --group [LISTGROUP]
		                        查询主机组
		  -T [LISTTEMP], --template [LISTTEMP]
		                        查询模板信息
		  -A ADDGROUP, --add-group ADDGROUP
		                        添加主机组
		  -C 192.168.2.1 test01,test02 Template01,Template02, --add-host 192.168.2.1 test01,test02 Template01,Template02
		                        添加主机,多个主机组或模板使用分号
		  -d 192.168.2.1, --disable 192.168.2.1
		                        禁用主机
		  -D 192.168.2.1 [192.168.2.1 ...], --delete 192.168.2.1 [192.168.2.1 ...]
		                        删除主机,多个主机之间用分号
		  -v, --version         show program's version number and exit
		
		
###参考：
1.[zabbix 官方api](https://www.zabbix.com/documentation/2.0/manual/appendix/api/api)

2.["王伟" 博客](http://wangwei007.blog.51cto.com/68019/1249770)

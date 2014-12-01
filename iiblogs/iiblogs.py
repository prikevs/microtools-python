#!/usr/bin/python
#coding=utf-8

import MySQLdb
import sys
import getopt
import os

HOST = 'localhost'
USER = 'root'
PASSWORD = 'yjfs1002'
DBNAME = 'iiblogs'

BROWSER = 'chromium-browser'

def Usage():
	print "iiblogs [name] |  [option] [name]"
	print "\tiiblogs [name]				open his blog"
	print '\tiiblogs [-a|--add] [name]		add new address'
	print '\tiiblogs [-d|--del] [name]		delete address'
	print '\tiiblogs [-m|--modify] [name]		modify the address'
	print '\tiiblogs [-c|--change_name] [newname] 	change the name'
	print '\tiiblogs [-l|--list]			list all'
	print '\tiiblogs [-h|--help]			help infomation'
	return

def Connect():
	conn = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWORD, db=DBNAME, charset = 'utf8')
	return conn

def Add(name):
	conn = Connect()
	mycursor = conn.cursor()
	sql = "select name from blogs where name = %s"
	param = (name)
	n = mycursor.execute(sql, param)
	if n > 0:
		print 'This name exists'
		return
	addr = raw_input("blog's address:")
	sql = "insert into blogs values(null, %s, %s);"
	param = (name, addr)
	mycursor.execute(sql, param)
	conn.commit()
	conn.close()
	return;	
	
def Delete(name):
	conn = Connect()
	mycursor = conn.cursor()
	sql = "delete from blogs where name = %s"
	param = (name)
	mycursor.execute(sql, param)
	conn.commit()
	conn.close()
	return;

def Opensite(args):
	conn = Connect()
	mycursor = conn.cursor()
	sql = "select address from blogs where name=%s"
	weblist = []
	fail = []
	webs = ' '
	for name in args:
		param = (name)
		n = mycursor.execute(sql, param)
		if n < 1:
			print "'%s' does not exist" % (name)
			fail.append(name)
			continue
		else:
			print "'%s' OK." % (name)
		for one in mycursor.fetchone():
			one = one.encode("utf-8")    #utf8 ------------
			weblist.append(one)			
	if not len(weblist):
		return
	for index, item in enumerate(weblist):
		webs = webs + ' ' + item
	last = BROWSER + webs + ' &'
	os.system(last)
	conn.close()
	return

def List():
	conn = Connect()
	mycursor = conn.cursor()
	sql = "select name, address from blogs"
	mycursor.execute(sql)
	for res in mycursor.fetchall():
		print res[0], ':	', res[1]
	conn.close()
	return

def Modify(name):
	conn = Connect()
	mycursor = conn.cursor()
	sql = 'select name from blogs where name=%s'
	param = (name)
	n = mycursor.execute(sql, param)
	if n < 1:
		print "This name does not exist"
		return
	new = raw_input("please input the new address:")
	sql = "update blogs set address=%s where name=%s"
	param = (new, name)
	mycursor.execute(sql, param)
	conn.commit()
	conn.close()
	return

def Changename(name):
	conn = Connect()
	mycursor = conn.cursor()
	sql = 'select name from blogs where name=%s'
	param = (name)
	n = mycursor.execute(sql, param)
	if n < 1:
		print "This name does not exist"
		return
	new = raw_input("please input the new name:")
	sql = "update blogs set name=%s where name=%s"
	param = (new, name)
	mycursor.execute(sql, param)
	conn.commit()
	conn.close()
	return
		
try:
	opts, args = getopt.getopt(sys.argv[1:], 'lha:d:m:c:', ['list', 'help', 'add', 'del', 'modify', 'change'])
except getopt.GetoptError:
	Usage()
	sys.exit()
for o, a in opts:
#a = a.decode("gbk").encode("utf-8")
	if o in ('-h', '--help'):
		Usage()
		sys.exit()
	if o in ('-a', '--add'):
		Add(a)
		sys.exit()
	if o in ('-d', '--del'):
		Delete(a)	
		sys.exit()
	if o in ('-l', '--list'):
		List()
		sys.exit()
	if o in ('-m', '--modify'):
		Modify(a)
		sys.exit()
	if o in ('-c', '--change'):
		Changename(a)
		sys.exit()
if len(args) == 0:
	Usage()
else:
	Opensite(args)



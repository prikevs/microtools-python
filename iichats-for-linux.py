#!/usr/bin/python
#coding:utf8

import threading
import socket
import time
import os
import sys
import signal
from readline import get_line_buffer
BUFSIZE = 1024
BACKPORT = 7789
CHATPORT = 7788
START = '>>'
INIT = '>>'
users = {}
ips = {}

class Data():
	def gettime(self):
		return time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
	def getip(self):
		ip = os.popen("/sbin/ifconfig | grep 'inet addr' | awk '{print $2}'").read()
	   	ip = ip[ip.find(':')+1:ip.find('\n')]
		return ip
	def handlebc(self, data):
		data = data[5:]	
		res = data.split('#opt:')
		return res
	def makebc(self, name, switch):
		data = 'name:%s#opt:%d' % (name, switch)
		return data
	def handlechat(self, data):
		msg = '\n' + self.gettime() + '\n' +'from '+ data + '\n'
		return msg
	def makechat(self, data, name):
		return name + ':' + data

class Back(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.data = Data()
		self.addrb = ('255.255.255.255', BACKPORT)
		self.addrl = ('', BACKPORT)
		self.name = socket.gethostname()
		self.ip = self.data.getip()
		self.thread_stop = False
	def status(self, name, switch):
		if switch == 0:
			status = 'offline'
		elif switch == 1:
			status = 'online'
		if outmutex.acquire(1):
			sys.stdout.write('\r'+' '*(len(get_line_buffer())+len(START))+'\r')
			print '[status] '+name+' '+status
			sys.stdout.write(START+get_line_buffer())
			sys.stdout.flush()
			outmutex.release()
	def broadcast(self, switch):
		bsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		bsock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		data = self.data.makebc(self.name, switch)	
		bsock.sendto(data, self.addrb)
		bsock.close()
	def response(self, addr, switch):
		rsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		data = self.data.makebc(self.name, switch)	
		rsock.sendto(data, (addr, BACKPORT))
		rsock.close()
	def check(self):
		if usermutex.acquire():
			ips.clear()
			users.clear()
			usermutex.release()
		self.broadcast(1)
	def	run(self):
		lsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		lsock.bind(self.addrl)
		self.broadcast(1)
		while not self.thread_stop:
			data, addr = lsock.recvfrom(BUFSIZE)
			datalist = self.data.handlebc(data)
			if usermutex.acquire(1):
				if datalist[1] == '0':
					if ips.has_key(addr[0]):
						if anoun == 1:
							self.status(datalist[0], 0)
						del ips[addr[0]]
						del users[datalist[0]]
				elif datalist[1] == '1':
					if anoun == 1 and datalist[0] != self.name:
						self.status(datalist[0], 1)
					users[datalist[0]] = addr[0]
					ips[addr[0]] = datalist[0]
					self.response(addr[0], 2)
				elif datalist[1] == '2':
					if anoun == 1 and datalist[0] != self.name:
						self.status(datalist[0], 1)
				  	users[datalist[0]] = addr[0]
				 	ips[addr[0]] = datalist[0]
				usermutex.release()
		lsock.close()
	def stop(self):
		self.broadcast(0)
		self.thread_stop = True

class Listen(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.addr = ('', CHATPORT)
		self.name = socket.getfqdn(socket.gethostname())
		self.data = Data()
		self.thread_stop = False
	def ans(self, addr): #waiting....
		return
	def run(self):
		lsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		lsock.bind(self.addr)
		while not self.thread_stop:
			data, addr = lsock.recvfrom(BUFSIZE)
			msg = self.data.handlechat(data)
			if outmutex.acquire(1):
				sys.stdout.write('\r'+' '*(len(get_line_buffer())+len(START))+'\r')
				print msg
				sys.stdout.write(START+get_line_buffer())
				sys.stdout.flush()
				outmutex.release()
		lsock.close()
	def stop(self):
		self.thread_stop = True
			
class Start():
	def __init__(self):
		self.name = socket.getfqdn(socket.gethostname())
		self.data = Data()
		self.listen = Listen()
		self.back = Back()
		print '*******   iichats   ********'
		print '     Written by Kevince     \n'
		print 'This is ' + self.name
		print self.data.gettime()+'\n'
	def helpinfo(self):
		if outmutex.acquire(1):
			print "use ':' to use options"
			print "\t:exit\t\t\texit iichats"
			print "\t:list\t\t\tlist online users"
			print "\t:quit\t\t\tquit the chat mode"
			print "\t:chat [hostname]\tchatting to someone"
			print "\t:set status [on|off]\tturn on/of status alarms"
			print "\t:check\tcheck online PCs"
			outmutex.release()
	def refresh(self):
		if outmutex.acquire(1):
			print '\n******Onlinelist******'
			for key in users:
				print key
			print '**********************\n'
			outmutex.release()
	def chatting(self):
		csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		if outmutex.acquire(1):
			print "use ':help' to get help information"
			outmutex.release()
		name = ''
		address = ''
		global anoun
		global START
		while True:
			arg = raw_input(START)
			if arg[0:5] == ':quit' and START != INIT:
				name = ''
				address = ''
				START = INIT
			elif arg[0] == ':' and START == INIT:
				if arg[1:] == 'exit':
					break
				elif arg[1:5] == 'list':
					self.refresh()
					continue
				elif arg[1:12] == 'set status ':
					if arg[12:] == 'on':
						anoun = 1
					elif arg[12:] == 'off':
						anoun = 0
					continue
				elif arg[1:5] == 'help':
					self.helpinfo()
					continue
				elif arg[1:6] == 'check':
					self.back.check()
					print 'checking the list...'
					time.sleep(3)
					if outmutex.acquire(1):
						outmutex.release()		
					self.refresh()
				elif arg[1:6] == 'chat ':
					name = arg[6:]
					if usermutex.acquire(1):
						userlist = users.keys()
						usermutex.release()
					if name not in userlist:
						if outmutex.acquire(1):
							print 'this host does not exist'
							outmutex.release()
						continue
					address = (users.get(name), CHATPORT)
					if outmutex.acquire(1):
						print 'now chatting to ' + name+" ,use ':quit' to quit CHAT mode"
						START = name + INIT
						outmutex.release()
				else:
					if outmutex.acquire(1):
						print "invalid input, use ':help' to get some info"
						outmutex.release()
			else:
				if not len(address):
					if outmutex.acquire(1):
						print "you can CHAT to someone, or use ':help'"
						outmutex.release()
					continue
				data = arg
				msg = self.data.makechat(data, self.name)
				csock.sendto(msg, address)
		csock.close()
	def start(self):
		self.back.setDaemon(True)
		self.back.start()
		self.listen.setDaemon(True)
		self.listen.start()
		self.chatting()
		self.back.stop()
		self.listen.stop()
		sys.exit()

usermutex = threading.Lock()
outmutex = threading.Lock()
anoun = 1
s = Start()
s.start()

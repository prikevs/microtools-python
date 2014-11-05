#!/usr/bin/python

import sys
import getopt

content = []
headfile = "/home/kevince/Documents/acm/head/acmhead.h" #the directory of the headfile

#load file head.h and save it with a list
def loadcontent():
	f = open(headfile)
	lines = f.readlines()
	for line in lines:
		content.append(line)

def Write(filename):
	f = open(filename, "w")
	for index, val in enumerate(content):
		f.write(val)
	f.close()

def End(al):
	num = ord(al) - ord('A') + 1
	if num < 1 or num > 26:
		print 'A-Z, please'
		return
	for i in range(0, num):
		name = chr(ord('A') + i) + '.cpp'
		Write(name)
	return

def Num(num):
	num = int(num)
	if num < 1 or num > 26:
		print '1-26, please'
		return
	for i in range(0, num):
		name = chr(ord('A') + i) + '.cpp'
		Write(name)
	return
		

def Usage():
	print "\n"
	print "iiacm-filemaker [fliename]\n"
	print "or\n"
	print "iiacm-filemaker -n | -e\n"
	print "   -n  number of files\n"
	print "   -e  endplace of files\n"
	return

def Make(args):
	Write(args[0]+'.cpp')
	return

#main function
def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'e:n:', ['--end', '--num'])
	except getopt.GetoptError:
		Usage()
		sys.exit()	
	loadcontent()  #loadcontent
	for o, a in opts:
		if o in ('-e', '--help'):
			End(a)
			sys.exit()
		if o in ('-n', '--num'):
			Num(a)
			sys.exit()
	if len(args) == 0:
	  	Usage()
	else:
		Make(args)
	


if __name__ == '__main__':
	main()

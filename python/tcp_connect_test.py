import os
import sys
import socket
import time
import datetime
import getopt
import string

#make a single one connection test
#and return the microseconds of connec time
def calcConnectTime(addr,port):
    #address tuple
    sockAddr = (addr,port)
    try:
    	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except Exception, e:
    	print str(e)
    	return -1

    #connect
    startTime = datetime.datetime.now()
    sock.connect(sockAddr)
    t = datetime.datetime.now() - startTime
    #close
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    return t.microseconds/1000

#make the whole connection test for specified addr-port tuple
#times indicate the time we will make
#intime indicate how long we should complete
def makeTcpConnectTest(addr,port,times,intime):
	result = []
	assert(times>0 and intime>0)
	perTime = intime/times
	for x in xrange(1,times+1):
		escaped = calcConnectTime(addr,port)
		r = (x,escaped)	
		result.append(r)
		time.sleep(perTime)
	return result


#main
if __name__ == '__main__':
	tcpAddr = ""
	tcpPort = 0
	connTimes = 1
	connTime = 1

	accquireArgs = ["addr=","port=","time=","count="]
	try:
		ops,args = getopt.getopt(sys.argv[1:],"",accquireArgs)
	except Exception, e:
		print str(e)
		sys.exit(1)

	print ops

	if(len(ops) != len(accquireArgs)):
		print "invalid params"
		sys.exit(1)

	for k,v in ops:
		lk = string.lower(k)
		if lk == "--addr":
			tcpAddr = v
		elif lk == "--port":
			tcpPort = int(v)
		elif lk == "--time":
			connTime = int(v)
		elif lk == "--count":
			connTimes = int(v)
		else:
			print "unuseful arg",k

	result = makeTcpConnectTest(tcpAddr,tcpPort,connTimes,connTime)
	
	total = 0	
	failed = 0
	for k,v in result:
		print k , "cost",str(v) ,"ms"
		t = int(v)
		if t == -1:
			connTimes = connTimes-1
			failed = failed + 1 
		else:
			total = total + int(v)

	print "Failed connection: ",failed," times"
	print "Average connect time cost : ",float(total/connTimes),"ms"

else:
	print "this module do not support run in other program"
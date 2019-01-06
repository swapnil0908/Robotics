#!/usr/bin/env python




import rospy
import roslib
import socket
import sys

from geometry_msgs.msg import Twist
from std_msgs.msg import String


globalQueue=[]
class Server:
	message=""
	
	def __init__(self):
		rospy.init_node('Server_Main')
		self.host = '149.125.148.129'  
		self.portNo=8888
		self.s=None #socket
		self.queue=None
		self.queuePtr=0;
		self.pub = rospy.Publisher('chatter', String, queue_size=10)
		self.queue=list([])
		self.createServer()

	def createServer(self):
		self.queue=list([])
		self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print("Socket Created")
		try:
			self.s.bind((self.host, self.portNo))
		except socket.error as err:
			print('Bind Failed, Error Code: ' + str(err[0]) + ', Message: ' + err[1])
			sys.exit()
		print('Socket Bind Success!')

		self.s.listen(10)
		print('Socket is now listening')

		while 1:
			conn, addr = self.s.accept()
			print('Connect with ' + addr[0] + ':' + str(addr[1]))
			buf = conn.recv(64)
			self.queue.append(str(buf.decode('utf-8')))
			#print(self.queue)
			print("Queued"+str(buf.decode('utf-8')))
			globalQueue.append(str(buf.decode('utf-8')))
			self.pub.publish(str(buf.decode('utf-8')))

			#self.moveBase()



		self.s.close()


if __name__ == '__main__':
	Server()



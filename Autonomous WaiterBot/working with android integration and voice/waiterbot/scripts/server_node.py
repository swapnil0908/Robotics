#!/usr/bin/env python




import rospy
import roslib
import socket
import sys

from geometry_msgs.msg import Twist

class Server:
	def __init__(self):
		rospy.init_node('Server')
		self.host = '149.125.84.244'  
		self.portNo=8888
		self.s=None #socket
		self.queue=None
		self.queuePtr=0;
		self.cmd_vel = rospy.Publisher("mobile_base/commands/velocity", Twist, queue_size=10)
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
			self.moveBase()



		self.s.close()

	def moveBase(self):
		if self.queuePtr > len(self.queue) or len(self.queue)==0:
			return
		task=self.queue[self.queuePtr]
		direction=task.split(":")[0]
		vel_info=Twist()
		vel_info.linear.y=0
		vel_info.linear.z=0
		vel_info.angular.x=0
		vel_info.angular.y=0
		vel_info.angular.z=0
		vel_info.linear.x=0
		if direction=="1":
			vel_info.linear.x=0.5
		else:
			vel_info.linear.x=-0.5
		self.cmd_vel.publish(vel_info)
		self.queuePtr=self.queuePtr+1
		rospy.sleep(1)

if __name__ == '__main__':
	Server()



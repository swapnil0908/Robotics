#!/usr/bin/env python




import rospy
import roslib
import socket
import sys
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import server_main as sm

class ServerListener:
	message=""
	
	def __init__(self):
		#self.msgServer=sm.Server()
		self.taskQueue=[]
		rospy.init_node('listener', anonymous=True)
		print('Server Listener')
		rospy.Subscriber("chatter", String, self.callback)
		rospy.spin()

	def callback(self,data):
		self.taskQueue.append(str(data))
		print("Queue Status:"+str(self.taskQueue)+"\n")


if __name__ == '__main__':
	ServerListener()
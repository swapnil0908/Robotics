#!/usr/bin/env python

import rospy
import random
import sys
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math
PI = 3.1415926535897

count = 0
temp = 1
def turn_left():
	global count
	global temp
	move.angular.z = 0.52
	count += 1
	if count == 24: 
		temp = 1

def turn_right():
	global count
	move.angular.z = -0.52

def turn_around():
	global count
	count += 1
	move.angular.z = 3.5
	rospy.sleep(1)

def move_straight():
	move.linear.x = 0.2
	move.angular.z = 0
	

def laser(msg):
	global temp
	print msg.ranges[0]
	if msg.ranges[0] < 0.5:
		print (msg.ranges[0])	
		move.linear.x = 0
		turn_left()
		move.linear.x = 0


	elif msg.ranges[0] > 0.5:
		if msg.ranges[0] > 1.2 and count > 24 and temp == 1:
			move.linear.x = 0
			turn_right()
			move.linear.x = 0
			temp = 0
		else: 
			move_straight()
		
		

		
def main():
	global move
        rospy.init_node('map_scan', anonymous=True)
	sub = rospy.Subscriber('/scan', LaserScan, laser)
        pub = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
        rate = rospy.Rate(10)
	move = Twist()
	while not rospy.is_shutdown():
            pub.publish(move)
            rate.sleep()
	rospy.spin()

if __name__ == '__main__':
	main()
    


   


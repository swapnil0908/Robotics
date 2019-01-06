#!/usr/bin/env python

import rospy
import sys
from turtlesim.msg import Pose
from turtlesim.srv import Spawn, Kill
from std_srvs.srv import Empty
from geometry_msgs.msg import Twist
from math import sqrt, pow, atan2
import random
PI = 3.1415926535897
avoid = 0
distance_tolerance = 1

runner_x = 0
runner_y = 0
hunter_x = 0
hunter_y = 0
runner_angle = 0
hunter_angle = 0


def hunterPose(data):
    global hunter_x, hunter_y, hunter_angle
    hunter_x = data.x
    hunter_y = data.y
    hunter_angle = data.theta


def runnerPose(data):
    global runner_x, runner_y, runner_angle, avoid
    #if the runner is outside the range 1 to 10 then set avoid = 1 to avoid collision with the wall
    if data.x <= 1 or data.x >= 10 or data.y <= 1 or data.y >= 10:
	    avoid = 1
    runner_x = data.x
    runner_y = data.y
    runner_angle = data.theta


def spawnTurtle():
    global runner_x, runner_y, runner_angle
    runner_x = random.randint(1, 10)
    runner_y = random.randint(1, 10)
    runner_angle = random.uniform(0,20)
    spawn(runner_x,runner_y,runner_angle,"runner")
    

def runner_action():
    #assign the runner linear and angular velocities as per requirements
    global run
    global avoid
    #print("running")
    run.linear.x = 1
    run.linear.y = 0
    run.linear.z = 0
    run.angular.z = random.uniform(-1,1)
    pub1.publish(run)

def hunter_action():
    #assign the hunter linear and angular velocities as per requirements
    global hunt
    hunt.linear.x = 1
    hunt.linear.y = 0
    hunt.linear.z = 0
    hunt.angular.z = random.uniform(-1,1)
    pub2.publish(hunt)
    #print("hunting")

def hunting():
    #calculate the distance between hunter and runner
    global runner_x, runner_y, hunter_x, hunter_y
    distance = euclideanDistance(runner_x,runner_y, hunter_x, hunter_y)
    #print "distance: ", distance

    angle = atan2(runner_y - hunter_y, runner_x - hunter_x)	
    #print "theta: ", angle
    #if distance greater than 1 assign linear velocity 1 and set angular velocity with respect to runner
    if distance >= distance_tolerance:
	hunt.linear.x = 1
	hunt.linear.y = 0
	hunt.linear.z = 0
	hunt.angular.x = 0
	hunt.angular.y = 0
	hunt.angular.z = angle - hunter_angle
    	pub2.publish(hunt)
    #if distance less than 1 kill the runner, clear the board and spawn new runner again
    elif distance < distance_tolerance:
	#print "Caught the runner!!!"
	kill("runner")
	clear()
	spawnTurtle()
	

def euclideanDistance(x2,y2,x1,y1):
    return sqrt(pow((x2-x1),2) + pow((y2-y1),2))
 
def reverse():

    run.linear.x = -1
    run.linear.y = 0
    run.linear.z = 0
    run.angular.x = 0
    run.angular.y = 0
    run.angular.z = 0
  
    pub1.publish(run)
    rospy.sleep(2)

   
def avoidCollision():
    global direction	

    speed = 180
    angle = random.uniform(45,180)

    angular_speed = speed*2*PI/360
    relative_angle = angle*2*PI/360
    
    run.linear.x = 0
    run.linear.y = 0
    run.linear.z = 0
    run.angular.x = 0
    run.angular.y = 0

	
    run.angular.z = abs(angular_speed)
    
    t0 = rospy.Time.now().to_sec()
    current_angle = 0
    
    
    while(current_angle < relative_angle):
	pub1.publish(run)
	t1 = rospy.Time.now().to_sec()
	current_angle = angular_speed*(t1-t0)

    run.angular.z = random.uniform(-1,1)
    run.linear.x = 0.5
    pub1.publish(run)
    rospy.sleep(2)
		


def hunt_begin():

    global avoid
    
    #reset()
    spawnTurtle()
    
    while not rospy.is_shutdown():	
	#print "The hunt begins!"
	
	runner_action()
     
	hunter_action()
	
        hunting()

	if avoid == 1:
		reverse()
		avoidCollision()
		avoid = 0


if __name__ == '__main__':
    try:
        global rate, run, hunt
        rospy.init_node('turtlehunt', anonymous=True)
        pub1 = rospy.Publisher('/runner/cmd_vel', Twist, queue_size = 10)
	pub2 = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 10)
        rospy.Subscriber("/turtle1/pose", Pose, hunterPose)
        rospy.Subscriber("/runner/pose", Pose, runnerPose)
        rate = rospy.Rate(0.5)
        reset = rospy.ServiceProxy('/reset', Empty)
        clear = rospy.ServiceProxy('/clear', Empty)
        spawn = rospy.ServiceProxy('/spawn', Spawn)
        kill = rospy.ServiceProxy('/kill', Kill)
	run = Twist()
	hunt = Twist()
	
        hunt_begin()

    except rospy.ROSInterruptException:
	pass

#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def goto(x,y):

    temp = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    temp.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.position.z = 0.0
    goal.target_pose.pose.orientation.w = 1.0

    temp.send_goal(goal)
    wait = temp.wait_for_result()
    if not wait:
        print "Error!"
        rospy.signal_shutdown()
    else:
        return temp.get_result()

if __name__ == '__main__':
    try:
        rospy.init_node('goto_py')

	result = goto(-3.00,10.9)
        if result:
            print "Reached!"

	result = goto(7.67,9.11)
        if result:
            print "Reached!"
	
	result = goto(3.96,1.16)
        if result:
            print "Reached!"

    except rospy.ROSInterruptException:
            print "finished!"

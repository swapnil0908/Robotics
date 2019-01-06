#!/usr/bin/env python



import rospy, cv2, cv_bridge, numpy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import *
from geometry_msgs.msg import Point
import pyaudio
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient

class Follower:

	def __init__(self):

		self.bridge = cv_bridge.CvBridge()
		#cv2.namedWindow("window", 1)
		self.cmd_vel_pub = rospy.Publisher('mobile_base/commands/velocity',
		    Twist, queue_size=1)
		self.image_sub = None
		self.colorDetector_sub=None
		self.taskQueue=[]
		self.currColString=''
		self.isMoving=False
		self.twist = Twist()
		self.counter=0
		self.returnBack=0
		self.turnBack=False
		self.colorArr1=[]
		self.colorArr2=[]
		self.currColor=2
		self.colorArr=[]
		self.startMotion=False
		self.cnt=0
		self.ptr=0
		self.rotCoeff=-1
		self.soundhandle = SoundClient()
		rospy.Subscriber("chatter", String, self.callback)
		self.init_Move()
		

	def init_Move(self):
		#self.movementController()
		self.listenRequests()

	def unregisterSub(self):
		self.cnt=self.cnt+1
		print("In unregisterSub COUNT="+str(self.cnt))
		print("Color="+str(self.currColor)+" turnBack="+str(self.turnBack))
		self.image_sub.unregister()
		if self.turnBack==True:
			self.turnBackMotion()
		

	def turnBackMotion(self):
		self.cnt=self.cnt+1
		print("In turnBackMotion COUNT="+str(self.cnt))
		print("Move back")
		print("Waiting...")

		rospy.sleep(1)
		self.soundhandle.say('Please pick order for table number '+self.currColString+' I will wait here for thirty seconds', 'voice_kal_diphone')
		rospy.sleep(1)
		rospy.sleep(8)
		self.move("west",180)
		self.moveAlongLine(2)

	def callback(self,data):
		self.taskQueue.append(str(data))
		self.colorArr.append(int(str(data).split(":")[2]))
		print("Queue Status:"+str(self.taskQueue)+"\n")


	def unregisterColorSub(self):
		self.colorDetector_sub.unregister()
		self.moveAlongLine(1)


	def listenRequests(self):
		while 1:
			while self.ptr!=len(self.colorArr):
				if len(self.colorArr)==0:
					continue
				self.currColor=self.colorArr[self.ptr]
				self.detectColoredLine()
				while self.cnt!=4:
					pass
				self.cnt=0
				self.ptr=self.ptr+1

		




	def registerSub(self):
		self.image_sub = rospy.Subscriber('camera/rgb/image_raw',
			Image, self.image_callback)

	#all micro tasks
	def moveAlongLine(self,line_no):
		#0, 100, 100), cv::Scalar(10, 255, 255) #red
		#[45, 100, 100], [75, 255,255] #green
		#[110,50,50]), [130,255,255] # blue
		line_no=self.currColor

		if line_no==1:
			self.colorArr1=[45, 100, 100]
			self.colorArr2=[75, 255,255]

		if line_no==2:
			self.colorArr1=[0, 100, 100]
			self.colorArr2=[10, 255, 255]

		if line_no==3:
			self.colorArr1=[110,50,50]
			self.colorArr2=[130,255,255]
		self.image_sub = rospy.Subscriber('camera/rgb/image_raw',
		Image, self.image_callback)


	def detectColoredLine(self):
		if self.currColor==1:
			self.currColString="one"
		elif self.currColor==2:
			self.currColString="two"
		else:
			self.currColString="three"
		
		rospy.sleep(1)
		self.soundhandle.say('Please place order for table number '+self.currColString+' I will wait here for thirty seconds', 'voice_kal_diphone')
		rospy.sleep(1)
		rospy.sleep(5)
		self.cnt=self.cnt+1
		print("In detectColoredLine COUNT="+str(self.cnt))
		line_no=self.currColor

		"""if self.ptr!=0:
			if self.colorArr[self.ptr-1]==line_no:
				c=1
				while c!=20:
					self.rotatecont()
					c=c+1


				rospy.sleep(1)
				print("MOVE FOR SAME COLOR")"""

		if line_no==1:
			self.colorArr1=[45, 100, 100]
			self.colorArr2=[75, 255,255]
			self.rotCoeff=-1



			

		if line_no==2:
			self.colorArr1=[0, 100, 100]
			self.colorArr2=[10, 255, 255]
			if self.ptr==0:
				self.rotCoeff=-1
			elif self.colorArr[self.ptr-1]==1:
				self.rotCoeff=1
			else:
				self.rotCoeff=-1

		if line_no==3:

			self.colorArr1=[110,50,50]
			self.colorArr2=[130,255,255]
			self.rotCoeff=1
			if self.ptr==0:
				self.rotCoeff=-1
		

		self.colorDetector_sub=rospy.Subscriber('camera/rgb/image_raw',
		Image, self.detect_color_callback)



	def movementController(self):
		#self.moveToGoal(0.0282609660838,0.0342560425716)
		#self.move("east",90)
		"""for color in self.colorArr:
			print("COLOR="+str(color))
			self.currColor=color
			self.detectColoredLine()"""


		for color in self.colorArr:

			self.currColor=color
			self.detectColoredLine()
			while self.cnt!=4:
				pass
			self.cnt=0
			self.ptr=self.ptr+1


		








	def move(self,direction,angle):
		print("Angle="+str(angle))
		vel_info=Twist()
		vel_info.linear.y=0
		vel_info.linear.z=0
		vel_info.angular.x=0
		vel_info.angular.y=0
		vel_info.angular.z=0
		vel_info.linear.x=0
		if direction=="east" or direction=="west":
			angular_speed = 30*2*3.1416/360
			relative_angle = angle*2*3.1416/360
			current_angle=0
			time_prev = rospy.Time.now().to_sec()
			self.cmd_vel_pub.publish(vel_info)
			if direction=="east":
				vel_info.angular.z = -1*angular_speed
			else:
				vel_info.angular.z = angular_speed
			self.cmd_vel_pub.publish(vel_info)
			while(current_angle < relative_angle):
				self.cmd_vel_pub.publish(vel_info)
				time_now = rospy.Time.now().to_sec()
				current_angle = angular_speed*(time_now-time_prev)
			vel_info.linear.x=0
			vel_info.angular.z = 0
			self.cmd_vel_pub.publish(vel_info)
			#rospy.sleep(1)
		if direction=="north" or direction=="south":
			if direction=="north":
				vel_info.linear.x=0.3
			else:
				vel_info.linear.x=-0.3
			self.cmd_vel_pub.publish(vel_info)


	def rotatecont(self):
		
		vel_info=Twist()
		vel_info.linear.y=0
		vel_info.linear.z=0
		vel_info.angular.x=0
		vel_info.angular.y=0
		vel_info.angular.z=0
		vel_info.linear.x=0
		
		angular_speed = 30*2*3.1416/360
		relative_angle = 2*2*3.1416/360
		current_angle=0
		time_prev = rospy.Time.now().to_sec()
		self.cmd_vel_pub.publish(vel_info)
		
		vel_info.angular.z = self.rotCoeff*angular_speed
		
		self.cmd_vel_pub.publish(vel_info)
		while(current_angle < relative_angle):
			self.cmd_vel_pub.publish(vel_info)
			time_now = rospy.Time.now().to_sec()
			current_angle = angular_speed*(time_now-time_prev)
		
		self.cmd_vel_pub.publish(vel_info)
		#rospy.sleep(1)

			

	def image_callback(self, msg):
		#self.move("west")
		image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		#0, 100, 100), cv::Scalar(10, 255, 255) #red
		#[45, 100, 100], [75, 255,255] #green
		#[110,50,50]), [130,255,255] # blue
		lower_color = numpy.array(self.colorArr1)#lue
		upper_color = numpy.array(self.colorArr2) #blue
		mask = cv2.inRange(hsv, lower_color, upper_color)

		h, w, d = image.shape
		search_top = 3*h/4
		search_bot = 3*h/4 + 20
		mask[0:search_top, 0:w] = 0
		mask[search_bot:h, 0:w] = 0

		M = cv2.moments(mask)
		if M['m00'] > 0:
		        cx = int(M['m10']/M['m00'])
		        cy = int(M['m01']/M['m00'])
		        cv2.circle(image, (cx, cy), 20, (12,12,12), -1)
				#The proportional controller is implemented in the following four lines which
				#is reposible of linear scaling of an error to drive the control output.
		        err = cx - w/2
		        self.twist.linear.x = 0.5
		        self.twist.angular.z = -float(err) / 100
		        self.cmd_vel_pub.publish(self.twist)
		        #print('Linear X='+str(self.twist.angular.z))
		        self.isMoving=True
		else:
			self.isMoving=False

		#print("Moving Status="+str(self.isMoving))

		if self.isMoving==False:
			vel=Twist()
			if self.twist.linear.x!=0 and self.twist.angular.z!=0:
				self.twist.linear.x=1
				self.twist.linear.z=0
				self.cmd_vel_pub.publish(self.twist)
				print("Linear Movement")
				self.counter=self.counter+1

				if self.counter==18:
					self.counter=0
		    		self.twist=Twist()
		    		self.cmd_vel_pub.publish(self.twist)
		    		if self.turnBack==False:
		    			self.turnBack=True
		    		else:
		    			self.turnBack=False
		    		self.unregisterSub()


		
		cv2.imshow("window"+str(self.currColor), image)
		cv2.waitKey(3)

	def moveToGoal(self,xGoal,yGoal):

		#define a client for to send goal requests to the move_base server through a SimpleActionClient
		ac = actionlib.SimpleActionClient("move_base", MoveBaseAction)

		#wait for the action server to come up
		while(not ac.wait_for_server(rospy.Duration.from_sec(5.0))):
			rospy.loginfo("Waiting for the move_base action server to come up")
		goal = MoveBaseGoal()
		#set up the frame parameters
		goal.target_pose.header.frame_id = "map"
		goal.target_pose.header.stamp = rospy.Time.now()

		# moving towards the goal*/

		goal.target_pose.pose.position =  Point(xGoal,yGoal,0)
		goal.target_pose.pose.orientation.x = 0.0
		goal.target_pose.pose.orientation.y = 0.0
		goal.target_pose.pose.orientation.z = 0.0
		goal.target_pose.pose.orientation.w = 1.0

		rospy.loginfo("Sending goal location ...")
		ac.send_goal(goal)

		ac.wait_for_result(rospy.Duration(60))

		if(ac.get_state() ==  GoalStatus.SUCCEEDED):
			rospy.loginfo("You have reached the destination")
			return True

		else:
			rospy.loginfo("The robot failed to reach the destination")
			return False

	def detect_color_callback(self, msg):
		self.rotatecont()
		image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		hsv_yellow = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		lower_color = numpy.array(self.colorArr1)
		upper_color = numpy.array(self.colorArr2)
		lower_yellow = numpy.array([0,0,0])
		upper_yellow = numpy.array([50,50,100])
		mask = cv2.inRange(hsv, lower_color, upper_color)
		mask_yellow=cv2.inRange(hsv_yellow, lower_yellow, upper_yellow)
		h, w, d = image.shape
		search_top = 3*h/4
		search_bot = 3*h/4 + 20
		mask[0:search_top, 0:w] = 0
		mask[search_bot:h, 0:w] = 0
		mask_yellow[0:search_top, 0:w] = 0
		mask_yellow[search_bot:h, 0:w] = 0
		M = cv2.moments(mask)
		M_yellow=cv2.moments(mask_yellow)
		if M['m00'] > 0 :
			print("M[00]="+str(M['m00']))
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])
			err = cx - w/2
			print("COLOR DETECTED"+str(self.currColor))
			
			self.unregisterColorSub()
		cv2.imshow("Detecting colored line", image)
		cv2.waitKey(3)
rospy.init_node('line_follower')
follower = Follower()
rospy.spin()
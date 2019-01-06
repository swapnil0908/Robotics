#!/usr/bin/env python

import argparse
import roslib
import rospy
from geometry_msgs.msg import Twist
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
import pyaudio
from std_msgs.msg import String
from std_srvs.srv import *
import os
import commands

global pub
global speed


def parse_command(decoder):
	global msg, speed
	if decoder.hyp() != None:
	    print ([(seg.word, seg.prob, seg.start_frame, seg.end_frame)
	         for seg in decoder.seg()])
	    print ("Detected keyphrase, restarting search")
	    seg.word = seg.word.lower()
	    decoder.end_utt()
	    decoder.start_utt()
	    '''
	    if seg.word.find("full") > -1:
     	   	 if speed == 0.2:
		     msg.linear.x = msg.linear.x*2
		     msg.angular.z = msg.angular.z*2
		     speed = 0.4
	    if seg.word.find("half") > -1:
		 if speed == 0.4:
		     msg.linear.x = msg.linear.x/2
		     msg.angular.z = msg.angular.z/2
		     speed = 0.2
	    '''
     	    if seg.word.find("move") > -1:
		 msg.linear.x = speed
		 msg.angular.z = 0
     	    elif seg.word.find("right") > -1:
		 if msg.linear.x != 0:
		     if msg.angular.z < speed:
		         msg.angular.z += 0.05
		 else:
		     msg.angular.z = speed*2
     	    elif seg.word.find("west") > -1:
		 if msg.linear.x != 0:
		     if msg.angular.z > -speed:
		         msg.angular.z -= 0.05
		 else:
		     msg.angular.z = -speed*2
     	    elif seg.word.find("back") > -1:
		 msg.linear.x = -speed
		 msg.angular.z = 0
     	    elif seg.word.find("stop") > -1 or seg.word.find("halt") > -1:
		 msg = Twist()
	pub.publish(msg)
	
def init_pocketsphinx(model,lexicon,kwlist):
	config = Decoder.default_config()
	config.set_string('-hmm', model)
	config.set_string('-dict', lexicon)
	config.set_string('-kws', kwlist)

	stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1,rate=16000, input=True, frames_per_buffer=1024)
	stream.start_stream()

	decoder = Decoder(config)
	decoder.start_utt()

	while not rospy.is_shutdown():
	    buf = stream.read(1024)
	    if buf:
		  decoder.process_raw(buf, False, False)
	    else:
		  break
	    parse_command(decoder)
	
def VoiceNav():
	global msg, speed, pub, decoder
	if rospy.has_param("~model"):
	    model = rospy.get_param("~model")
	else:
	    rospy.loginfo("Loading the default acoustic model")
	    model = "/usr/share/pocketsphinx/model/hmm/en_US/hub4wsj_sc_8k"
	    rospy.loginfo("default acoustic model loaded")

	if rospy.has_param("~kwlist"):
	    kwlist = rospy.get_param("~kwlist")
	else:
	    rospy.logerr('No dictionary found.')
	    return
	   

	if rospy.has_param("~lexicon"):
	    lexicon = rospy.get_param("~lexicon")
	else:
	    rospy.logerr('kws cant run.')
	    return

	init_pocketsphinx(model,lexicon,kwlist)


def main():
	global pub,msg,speed
	rospy.init_node('voice_cmd_vel', anonymous=True)
	pub = rospy.Publisher('mobile_base/commands/velocity', Twist, queue_size=10)
	speed = 0.2
	msg = Twist()
	VoiceNav()

if __name__ == '__main__':
	main()

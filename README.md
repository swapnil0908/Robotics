## AUTONOMOUS WAITERBOT

### ABSTRACT
The aim of this project is to design a simulation for a TurtleBot to taking orders via speech recognition, serve customers and / or accept payments at restaurants and catering venues. The TurtleBot used in this project is a line follower and is able to travel to the target tables while avoiding obstacles such as other tables, chairs and even humans, it uses either laser scan or SONAR to detect the obstacles. The customer is be able to call the waiterBot for placing order by using a python based application interface / kiosk, that is on the table. After summoning the robot, the customer will place order verbally. Due to physical limitations on the payload capacity of the TurtleBot, the "WaiterBot" will only be able to serve specific items such as drinks or food items weighing less than 8 pounds. 

### METHODOLOGY
1. We assign different colored lines for different tables since we are using a line follower TurtleBot.
2. The camera angle on the TurtleBot is adjusted so that we are able to identify the colored lines on the ground and add a logic to move the TurtleBot forward as long as it gets the specific color input. We convert the data that 'sensor_msgs/Image' provides to a format that OpenCV can process.
3. Socket programming is used for the Android client and Python server to process asynchronous requests from different tables ( different colors ) on a first come first serve basis, while avoiding obstacles along the line / path.
4. We also use the 'sound_play' package for text to speech.

![waiterbot](https://user-images.githubusercontent.com/30382104/59148712-601e8700-89da-11e9-97df-0d24661d097e.gif)

### TOOLS USED
ROS Indigo, Python, TurtleBots, Android programming, Gazebo and SLAM

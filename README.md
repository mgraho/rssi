# Installation
1. Navigate to your catkin ws, e.g. cd ~/catkin_ws/src.
2. Clone this repository: git clone git@github.com:mgraho/rssi.git
3. Navigate one level up, i.e. cd ~/catkin_ws and run catkin_make.

# Usage
1. Set up parameters in rssi/config/config.yaml

2. Run one one device Roslaunch rssi main.launch

3. Run on every other device rosrun novo.py __ns=:`<name of the device>`
4. When you want to exit, select the window with Raspberries and pres Ctrl-c

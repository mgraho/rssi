
Navigate to your catkin ws, e.g. cd ~/catkin_ws/src.
Clone this repository: git clone git@github.com:mgraho/rssi.git
Navigate one level up, i.e. cd ~/catkin_ws and run catkin_make.
Set up parameters in rssi/config/config.yaml

run one one device Roslaunch rssi main.launch

run on every other device rosrun novo.py __ns=:<name of the device>

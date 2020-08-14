#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import rospy
import time
import numpy as np

from geometry_msgs.msg import Twist
from lidar_listener import LidarListener

# class for resueing the robot
# when it's lost, i.e. covariance
# of the amcl_pose is large
class SelfRescueMode(object):
    def __init__(self):
        # velocity publisher
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        # lidar listener
        self.scan_listener = LidarListener()
        
        # angular and linear velocity in rescue mode
        self.angular_vel = 0.2 #rad/s
        self.linear_vel = 0.2 #m/s

        # threshold showing there exists obstacles
        self.stop_threshold = 1.0 # if any thing within this range emerge in the laser scan, stop robot
        self.move_threshold = 5.0 # if all points in the front are farther then this value, go straight forward

        # parameter storing the width of the robot
        self.robot_width = 1.1
        self.open_area_pts = 40 # at least 40 points exist in an "open area"
        self.out_of_boundary_threshold = 5 #stop center detecting if y_distance > robot_width / 2 for more than 5 pts

        # paramter storing the current mode of the robot
        self.mode = "turning" # valid values: "turning", "forward"

        # define the variable to have velocity
        self.twist = Twist()

    def do_nothing(self):
        print("why we are here?")

    def do_nothing1(self):
        print("why we are here?")

    def move_straight_forward(self, linear_speed = 0.0):
        '''
        Move the vehicle straight forward under constant speed

		---
		Parameter

		linear_speed : float
            the linear speed of the vehicle
        '''
        #twist = Twist()
        self.twist.linear.x = linear_speed
        self.twist.angular.z = 0.0
        self.pub.publish(self.twist)


    def counter_clockwise_turn(self, angle= 5.0):
        '''
		turn the robot counter clockwise
		with a small angle (only roughly since 
		neither does the robot have sensors like 
		imu in use, nor is the robot localized
		
		---
		Parameter

		angle : float
		    the small angle we are going to turn. Unit is in degree, 
		    angle can also be negative, which will lead to clockwise turning
        '''
        self.twist.linear.x = 0.0
        self.twist.angular.z = self.angular_vel # 0.2 rad/s
        angle_rad = angle / 180.0 * np.pi 
        twist_time = abs(angle_rad / self.angular_vel)
        #print("angle_rad = %f, twist_time = %f" % (angle_rad,twist_time))
        # turn counter-clock wise
        self.pub.publish(self.twist)
        # sleep for sometime, so as to turn the robot
        time.sleep(twist_time)
        # stop the vehicle
        self.twist.linear.x = 0.0
        self.twist.angular.z = 0.0
        self.pub.publish(self.twist)
        time.sleep(0.1)


    

    def rescue(self):
        '''
        one step for rescueing the robot
        logic:
        
        check whether there exists any obstacle in the front
           of the robot

        if no obstacle exists:
            go straight forward
        else:
            if there exists open area to the left:
                turn counter-clock wise
            elif there exists open area to the right:
                turn clock-wise
            else:
                turn counter-clockwise     

        '''
        # get the latest scan data
        latest_scan = self.scan_listener.get_latest_scan()

        # check whether there exists any obstacle in the front
        middle_count = int(len(latest_scan.ranges) / 2)
        angle_min = latest_scan.angle_min
        angle_max = latest_scan.angle_max
        angle_increment = latest_scan.angle_increment
        
        no_obstacle = True

        front_distance_list = []
        '''
        out_of_boundary_count = 0

        for ii in range(middle_count,-1,-1):
            x_distance = abs(latest_scan.ranges[ii] * np.cos(angle_min + angle_increment * ii))
            y_distance = abs(latest_scan.ranges[ii] * np.sin(angle_min + angle_increment * ii))
            if y_distance > self.robot_width / 2: # check whether the point is in the front
                print("min index: %d, y_distance: %f" % (ii,y_distance))
                out_of_boundary_count += 1
                if out_of_boundary_count > self.out_of_boundary_threshold: # add a "out of boundary count" against inaccuracy in lidar measurement
                    break
            front_distance_list.append(x_distance)

        # reset the buffer
        out_of_boundary_count = 0

        for ii in range(middle_count,len(latest_scan.ranges)):
            x_distance = abs(latest_scan.ranges[ii] * np.cos(angle_min + angle_increment * ii))
            y_distance = abs(latest_scan.ranges[ii] * np.sin(angle_min + angle_increment * ii))
            if y_distance > self.robot_width / 2: # check whether the point is in the front
                print("max index: %d, y_distance: %f" % (ii,y_distance))
                out_of_boundary_count += 1
                if out_of_boundary_count > self.out_of_boundary_threshold: # add a "out of boundary count" against inaccuracy in lidar measurement
                    break
            front_distance_list.append(x_distance)
        '''
        for ii in range(int(middle_count / 2),int(middle_count / 2 * 3)):
            x_distance = abs(latest_scan.ranges[ii] * np.cos(angle_min + angle_increment * ii))
            y_distance = abs(latest_scan.ranges[ii] * np.sin(angle_min + angle_increment * ii))
            if y_distance <= self.robot_width / 2: # check whether the point is in the front
                front_distance_list.append(x_distance)

        if self.mode == "turning":
            if min(front_distance_list) > self.move_threshold:
                # we have find an open area, go straight forward
                self.mode = "forward"  
                self.move_straight_forward(self.linear_vel)
                print("going straight forward!")
                return
            #else:
            #    self.counter_clockwise_turn() # slowly turn counter-clockwise, try to find an open area
            #    return

        elif self.mode == "forward":
            if min(front_distance_list) > self.stop_threshold:
                # we are moving in an open area, keep going
                self.mode = "forward"
                self.move_straight_forward(self.linear_vel)
                return
            else:
                # there exists obstacle in the front, stop
                self.mode = "turning"
                self.move_straight_forward(0.0) # stop robot

        # robot meets obstacle if coming here
        # check whether there exists an open area 
        exist_open_area = False
        center_of_open_area = None
        for ii in range(0,len(latest_scan.ranges) - self.open_area_pts):
            if min(latest_scan.ranges[ii:ii+self.open_area_pts]) > self.move_threshold + 1.0:
                exist_open_area = True
                center_of_open_area = ii + self.open_area_pts / 2
                break

        if exist_open_area:
            print("Find open area, turn")
            self.counter_clockwise_turn(center_of_open_area * 0.25 - 90.0)
            self.mode = "turning"
            return
        else:
            # no open area exist, turn counter-clockwise for self-rescue
            print("Turn to find open area")
            self.mode = "turning"
            self.counter_clockwise_turn(45.0) # turn 45 degrees
            return


def main():
    rospy.init_node('self_rescue')
    self_rescuer = SelfRescueMode()
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        self_rescuer.rescue()
        rate.sleep()

if __name__ == "__main__":
    main()

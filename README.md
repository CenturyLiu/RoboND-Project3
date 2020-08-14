# RoboND-Project3
Implementation of Project 3 of [udacity robot software nanodegree](https://blog.udacity.com/2019/01/learn-robotics-engineering-program.html)

## Installation

Download the packages into your ROS workspace. Please unzip the "classroom_map.pgm.zip" in the [locate_my_robot/maps folder](https://github.com/CenturyLiu/RoboND-Project3/tree/master/locate_my_robot/maps). (The map is too big to be uploaded directly onto github)

## AMCL parameters

This section discusses the parameters I tuned in order to increase the precision of the [ROS-amcl package](http://wiki.ros.org/amcl).

Parameters

- essential parameters to put amcl into use:
    
    |Parameter Name|Value|Comment|
    |---|---|---|
    |odom_frame_id|odom|Default by the amcl package|
    |odom_model_type|diff-corrected|choice suggested by Udacity class|
    |base_frame_id|robot_footprint|The base link for [my_robot](https://github.com/CenturyLiu/RoboND-Project3/blob/master/my_robot/urdf/my_robot.xacro)|
    |global_frame_id|map|Default by the amcl package|
    
- initial pose

    |Parameter Name|Value|Comment|
    |---|---|---|
    |initial_pose_x|0.0|based on initial position of the robot in [my_world](https://github.com/CenturyLiu/RoboND-Project3/blob/master/my_robot/launch/world.launch)|
    |initial_pose_y|0.0|based on initial position of the robot in [my_world](https://github.com/CenturyLiu/RoboND-Project3/blob/master/my_robot/launch/world.launch)|
    
- paramters to increase localization performance

    |Parameter Name|Value|Comment|
    |---|---|---|
    |min_particles|500|The number of min particles I used is 5 times the default value provided by the [ROS-amcl package](http://wiki.ros.org/amcl). Use a larger number of min particle can increase precision|
    |max_particles|5000|Default by the amcl package|
    |update_min_d|0.1|Only require 0.1 meter translational movement before next update. This parameter greately affects the precision according to my experiment.|
    |update_min_a|0.1|Only require 0.1 rad translational movement before next update. This parameter greately affects the precision according to my experiment.|
    |recovery_alpha_slow|0.001|Suggested value by the [ROS-amcl package](http://wiki.ros.org/amcl), has effect in dealing with the "robot-kidnap" issue according to my experiment.|
    |recovery_alpha_fast|0.1|Suggested value by the [ROS-amcl package](http://wiki.ros.org/amcl), has effect in dealing with the "robot-kidnap" issue according to my experiment.|
    
![amcl parameter tuning](https://github.com/CenturyLiu/RoboND-Project3/blob/master/amcl_parameter_demo.gif)

> left is the amcl performance with default parameters, right is the performance with tuned paramter described above. Clearly, the tuned parameter outperforms the default.

## Recover from kidnap

The robot is able to recover from kidnap in most cases. But it also occassionally fails to recover. 

![success recovery 1](https://github.com/CenturyLiu/RoboND-Project3/blob/master/successful_recovery_1.gif)
> Successful recovery from a wrong initial pose. To reproduce this feature, use the launch file "".

![success recovery 2](https://github.com/CenturyLiu/RoboND-Project3/blob/master/successful_recovery_2.gif)
> Successful recovery from a kidnap

![failure](https://github.com/CenturyLiu/RoboND-Project3/blob/master/successful_recovery_2.gif)
> Failure to recover after being kidnapped. The algorithm converge to a wrong place.

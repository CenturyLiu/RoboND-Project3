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
    |base_frame_id|robot_footprint|The base link for my_robot|
    |global_frame_id|map|Default by the amcl package|
    
- initial pose

    |Parameter Name|Value|Comment|
    |---|---|---|
    |initial_pose_x|0.0|based on initial position of the robot in [my_world](https://github.com/CenturyLiu/RoboND-Project3/blob/master/my_robot/launch/world.launch)|
    |initial_pose_y|0.0|based on initial position of the robot in [my_world](https://github.com/CenturyLiu/RoboND-Project3/blob/master/my_robot/launch/world.launch)|
    

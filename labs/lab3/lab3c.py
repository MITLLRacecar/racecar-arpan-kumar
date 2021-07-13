"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020

Lab 3C - Depth Camera Wall Parking
"""

########################################################################################
# Imports
########################################################################################

import sys
import cv2 as cv
import numpy as np

sys.path.insert(0, "../../library")
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################
wall_pt = 0
rc = racecar_core.create_racecar()
wall_distance = 0
angle = 0
speed = 0
dist_error = 0
area_stopping_range = 20
# Add any global variables here

########################################################################################
# Functions
########################################################################################


def start():
    """
    This function is run once every time the start button is pressed
    """
    # Have the car begin at a stop
    rc.drive.stop()

    # Print start message
    print(">> Lab 3C - Depth Camera Wall Parking")

def update():
    global wall_pt
    global wall_distance
    global angle
    global dist_error
    global speed
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    # TODO: Park the car 20 cm away from the closest wall with the car directly facing
    # the wall
    top_left_inclusive = (0, 0)
    bottom_right_exclusive = (rc.camera.get_height() * 2 //3, rc.camera.get_width())
    depth_image = rc.camera.get_depth_image()

    dist_image = rc_utils.crop(depth_image, top_left_inclusive, bottom_right_exclusive)
    dist_image = cv.GaussianBlur(dist_image, (5,5), 0   )
    wall_pt = rc_utils.get_closest_pixel(dist_image)
    wall_distance = dist_image[wall_pt[0]][wall_pt[1]]
    dist_error = wall_distance - 20

    angle = angle_controller()
    speed = throttle_controller()

    rc.drive.set_speed_angle(speed, angle)

def angle_controller():
    global wall_pt
    global wall_distance
    kP = 1
    angle = 0
    if wall_distance != 0.00: 
        error = wall_pt[1] - rc.camera.get_width() / 2
        angle = kP * 2 * error/rc.camera.get_width()
    return angle

def throttle_controller(): 
    #If within contour range, brake until acceleration = 0. 
    print('Within Throttle Controller')
    global dist_error
    global area_stopping_range
    max_speed = 0.30
    kP = 1
    speed = 0
    print(dist_error)
    # if we are farther than the stopping range, apply full power
    if dist_error > area_stopping_range : speed = max_speed
    # elif contour_area < goal_area: speed = -.1
    else :
        # else scale our power by our error clamped within the stopping range
        # error as a percentage instead of area
        scale = 1/(8*area_stopping_range)
        speed = kP * dist_error * scale

    if speed > max_speed : speed = max_speed
    elif speed < -max_speed : speed = -max_speed
    print(speed)
    return speed

########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()
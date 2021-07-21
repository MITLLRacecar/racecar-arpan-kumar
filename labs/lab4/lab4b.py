"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020

Lab 4B - LIDAR Wall Following
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

from enum import IntEnum

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# Add any global variables here

DIST = 45 
LEFT_WINDOW = (260, 280)
RIGHT_WINDOW = (80, 100)
# RIGHT_TOP_WINDOW = (50, 70)
# LEFT_TOP_WINDOW = (320, 340)
RIGHT_TOP_WINDOW = (30, 50)
LEFT_TOP_WINDOW = (310, 330)
FRONT_WINDOW = (-20, 20)
REAR_WINDOW = (170, 190)

class State(IntEnum):
    drive = 0

cur_state = State.drive

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
    print(">> Lab 4B - LIDAR Wall Following")


def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    # TODO: Follow the wall to the right of the car without hitting anything.
    global DIST, RIGHT_TOP_WINDOW, LEFT_TOP_WINDOW, RIGHT_WINDOW, LEFT_WINDOW, FRONT_WINDOW, REAR_WINDOW
    global cur_state
    
    scan = rc.lidar.get_samples()
    scan = (scan - 0.01) % 100000

    speed = 1
    angle = 0

    _, right_dist = rc_utils.get_lidar_closest_point(scan, RIGHT_WINDOW)
    _, left_dist = rc_utils.get_lidar_closest_point(scan, LEFT_WINDOW)
    _, right_top_dist = rc_utils.get_lidar_closest_point(scan, RIGHT_TOP_WINDOW)
    _, left_top_dist = rc_utils.get_lidar_closest_point(scan, LEFT_TOP_WINDOW)
    _, front_dist = rc_utils.get_lidar_closest_point(scan, FRONT_WINDOW)
    _, rear_dist = rc_utils.get_lidar_closest_point(scan, REAR_WINDOW)

    
    if cur_state == State.drive:
        if right_top_dist > left_top_dist:
            angle = angle_controller(right_top_dist, 1)            
        else:
            angle = angle_controller(left_top_dist, -1)

    if abs(angle) > 0.75:
        kP = 2
        speed = 1 / (abs(angle) * kP)
        speed = rc_utils.clamp(speed, -1, 1)

    rc.drive.set_speed_angle(speed, angle)   

    
def angle_controller(distance, direction):
    global DIST
    kP = 4
    angle = 0
    error = distance - DIST
    angle = kP * (error / DIST) * direction
    return rc_utils.clamp(angle, -1, 1)

########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()

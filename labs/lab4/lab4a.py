"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020

Lab 4A - LIDAR Safety Stop
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

rc = racecar_core.create_racecar()

# >> Constants
# The (min, max) degrees to consider when measuring forward and rear distances
FRONT_WINDOW = (-10, 10)
REAR_WINDOW = (170, 190)

DIST_STOPPING_RANGE = 200

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
    print(
        ">> Lab 4A - LIDAR Safety Stop\n"
        "\n"
        "Controls:\n"
        "    Right trigger = accelerate forward\n"
        "    Right bumper = override forward safety stop\n"
        "    Left trigger = accelerate backward\n"
        "    Left bumper = override rear safety stop\n"
        "    Left joystick = turn front wheels\n"
        "    A button = print current speed and angle\n"
        "    B button = print forward and back distances"
    )

def proportional_controller(forward_dist): 
    #If within contour range, brake until acceleration = 0. 
    global DIST_STOPPING_RANGE
    max_speed = 1
    kP = 10
    speed = 0
    print(forward_dist)
    # if we are farther than the stopping range, apply full power
    if forward_dist > DIST_STOPPING_RANGE: 
        speed = max_speed
    else :
        # else scale our power by our error clamped within the stopping range
        # error as a percentage instead of area
        scale = 1 / (kP * DIST_STOPPING_RANGE)
        speed = forward_dist * scale
    if speed > max_speed: 
        speed = max_speed
    elif speed < -max_speed:
        speed = -max_speed
    return speed 

def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    # Use the triggers to control the car's speed
    rt = rc.controller.get_trigger(rc.controller.Trigger.RIGHT)
    lt = rc.controller.get_trigger(rc.controller.Trigger.LEFT)
    speed = rt - lt

    # Calculate the distance in front of and behind the car
    scan = rc.lidar.get_samples()
    _, forward_dist = rc_utils.get_lidar_closest_point(scan, FRONT_WINDOW)
    _, back_dist = rc_utils.get_lidar_closest_point(scan, REAR_WINDOW)

    # TODO (warmup): Prevent the car from hitting things in front or behind it.
    # Allow the user to override safety stop by holding the left or right bumper.

    # Use the left joystick to control the angle of the front wheels
    angle = rc.controller.get_joystick(rc.controller.Joystick.LEFT)[0]

    # Print the current speed and angle when the A button is held down
    if rc.controller.is_down(rc.controller.Button.A):
        print("Speed:", speed, "Angle:", angle)

    # Print the distance of the closest object in front of and behind the car
    if rc.controller.is_down(rc.controller.Button.B):
        print("Forward distance:", forward_dist, "Back distance:", back_dist)

    
    if not (rc.controller.is_down(rc.controller.Button.RB) or rc.controller.is_down(rc.controller.Button.LB)):
        speed = proportional_controller(forward_dist)
        if speed <= 0.04:
            speed = 0


    rc.drive.set_speed_angle(speed, angle)
    
    # Display the current LIDAR scan
    #rc.display.show_lidar(scan)


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()

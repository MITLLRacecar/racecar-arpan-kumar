"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020
Lab 2B - Color Image Cone Parking
"""

########################################################################################
# Imports
########################################################################################

import sys
from typing import Counter
import cv2 as cv
import numpy as np

sys.path.insert(1, "../../library")
import racecar_core
import racecar_utils as rc_utils

from enum import IntEnum

class State(IntEnum):
    search = 0
    obstacle = 1
    approach = 2
    stop = 3

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# >> Constants
# The smallest contour we will recognize as a valid contour
MIN_CONTOUR_AREA = 30

# The HSV range for the color orange, stored as (hsv_min, hsv_max)
ORANGE = ((10, 100, 100), (20, 255, 255))

# The constant that determines the extent of the spiral's curvature 
SPIRAL_CONSTANT = 10

# >> Variables
speed = 0.0  # The current speed of the car
angle = 0.0  # The current angle of the car's wheels
contour_center = None  # The (pixel row, pixel column) of contour
contour_area = 0  # The area of contour

counter = 0
curr_state: State = State.search

########################################################################################
# Functions
########################################################################################


def update_contour():
    """
    Finds contours in the current color image and uses them to update contour_center
    and contour_area
    """
    global contour_center
    global contour_area

    image = rc.camera.get_color_image()

    if image is None:
        contour_center = None
        contour_area = 0
    else:
        # Find all of the orange contours
        contours = rc_utils.find_contours(image, ORANGE[0], ORANGE[1])

        # Select the largest contour
        contour = rc_utils.get_largest_contour(contours, MIN_CONTOUR_AREA)

        if contour is not None:
            # Calculate contour information
            contour_center = rc_utils.get_contour_center(contour)
            contour_area = rc_utils.get_contour_area(contour)

            # Draw contour onto the image
            rc_utils.draw_contour(image, contour)
            rc_utils.draw_circle(image, contour_center)

        else:
            contour_center = None
            contour_area = 0

        # Display the image to the screen
        rc.display.show_color_image(image)


def start():
    """
    This function is run once every time the start button is pressed
    """
    global speed
    global angle

    # Initialize variables
    speed = 0
    angle = 0

    # Set initial driving speed and angle
    rc.drive.set_speed_angle(speed, angle)

    # Set update_slow to refresh every half second
    rc.set_update_slow_time(0.5)

    # Print start message
    print(">> Lab 2B - Color Image Cone Parking")

def search():
    """
    Makes the robot move in a progressively larger spiral
    """
    global counter
    global SPIRAL_CONSTANT
    global angle
    global speed

    # Math to reduce nonlinearity in the inverse relationship
    counter += rc.get_delta_time()
    temp = (SPIRAL_CONSTANT/counter) ** 0.25
    angle = clamp(temp, -1, 1)
    speed = 1

def approach():
    """
    Approaches the cone through proportional control
    """
    global counter
    global angle
    global speed
    global contour_center

    angle = remap(contour_center[1], 0, 640, -1, 1)
    
    speed = remap(contour_center[0], 245, 340, 1, 0)
    #print(speed)
    #speed = 1

def remap(val, old_min, old_max, new_min, new_max):
    len1 = abs(old_min-old_max)
    len2 = abs(new_max-new_min)
    
    scale = len2/len1
    val = abs(val - old_min) * scale

    if (new_min > new_max):
        val = new_min - val
    else:
        val = new_min + val

    return val

def clamp(val, min, max):
    """
    Clamps values that are too high or too low to the min or max
    """
    if val > max:
        val = max
    elif val < min:
        val = min
    
    return val

def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    global speed
    global angle
    global contour_area
    global contour_center

    global curr_state

    # Search for contours in the current color image
    update_contour()

    # TODO: Park the car 30 cm away from the closest orange cone

    # Print the current speed and angle when the A button is held down
    if rc.controller.is_down(rc.controller.Button.A):
        print("Speed:", speed, "Angle:", angle)

    # Print the center and area of the largest contour when B is held down
    if rc.controller.is_down(rc.controller.Button.B):
        if contour_center is None:
            print("No contour found")
        else:
            print("Center:", contour_center, "Area:", contour_area)
    
    if curr_state == State.search:
        if contour_area > MIN_CONTOUR_AREA:
            curr_state = State.approach
        else:
            search()
    
    if curr_state == State.approach:
        if contour_area < MIN_CONTOUR_AREA:
            curr_state = State.search
        else:
            approach()

    # if rc.controller.get_trigger(rc.controller.Trigger.RIGHT) != 0:
    #     speed = 1
    #     angle = 0
    # elif rc.controller.get_trigger(rc.controller.Trigger.LEFT) != 0:
    #     speed = -1
    #     angle = 0
    # else:
    #     speed = 0
    #     angle = 0

    rc.drive.set_speed_angle(speed, angle)

    print("Center:", contour_center, "Area:", contour_area)

def update_slow():
    """
    After start() is run, this function is run at a constant rate that is slower
    than update().  By default, update_slow() is run once per second
    """
    # Print a line of ascii text denoting the contour area and x position
    if rc.camera.get_color_image() is None:
        # If no image is found, print all X's and don't display an image
        print("X" * 10 + " (No image) " + "X" * 10)
    else:
        # If an image is found but no contour is found, print all dashes
        if contour_center is None:
            print("-" * 32 + " : area = " + str(contour_area))

        # Otherwise, print a line of dashes with a | indicating the contour x-position
        else:
            s = ["-"] * 32
            s[int(contour_center[1] / 20)] = "|"
            print("".join(s) + " : area = " + str(contour_area))


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()
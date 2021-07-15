"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020

Phase 1 Challenge - Cone Slaloming
"""

########################################################################################
# Imports
########################################################################################

import sys
from typing import Counter
import cv2 as cv
import numpy as np

sys.path.insert(0, "../../library")
import racecar_core
import racecar_utils as rc_utils
from enum import IntEnum

class State(IntEnum):
    search  = 0
    approach_red = 1
    approach_blue = 2
    dodge_red = 3
    dodge_blue = 4
    stop = 5
    
########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

curr_state: State = State.search

speed = 0.0
angle = 0.0

#HSV Values
BLUE = ((100, 175, 200), (130, 255, 255))  # The HSV range for the color blue
RED  = ((170, 50, 50),(179, 255, 255))

##Contour stuff
MIN_CONTOUR_AREA = 300
contour_red_center = 0.0
contour_red_area = 0
contour_blue_center = 0.0
contour_blue_area = 0

# Distance to look beside center of cone
offset_dist = 150
turning = False
counter = 0
time_threshold = 0.75
dist = 50

########################################################################################
# Functions
########################################################################################


def start():
    """
    This function is run once every time the start button is pressed
    """
    # Have the car begin at a stop
    rc.drive.stop()
    curr_state = State.search
    # Print start message
    print(">> Phase 1 Challenge: Cone Slaloming")

def update_red_contour():
    """
    Finds contours in the current color image and uses them to update contour_center
    and contour_area
    """
    global contour_red_center
    global contour_red_area
    global RED

    image = rc.camera.get_color_image()

    if image is None:
        contour_center = None
        contour_area = 0
    else:
        # Find all blue and red contours
        contours_red = rc_utils.find_contours(image, RED[0], RED[1])

        # Select the largest contour of each color
        contour_red = rc_utils.get_largest_contour(contours_red, MIN_CONTOUR_AREA)
        
        #Find the contour area of each color
        red_area = rc_utils.get_contour_area(contour_red) if contour_red is not None else 0.0

        contour = contour_red

        if contour is not None:
            # Calculate contour information
            contour_red_center = rc_utils.get_contour_center(contour)
            contour_red_area = rc_utils.get_contour_area(contour)

            # Draw contour onto the image
            # rc_utils.draw_contour(image, contour)
            # rc_utils.draw_circle(image, contour_red_center)            
        else:
            contour_red_center = None
            contour_red_area = 0

        return contour
        

def update_blue_contour():
    """
    Finds contours in the current color image and uses them to update contour_center
    and contour_area
    """
    global contour_blue_center
    global contour_blue_area
    global BLUE

    image = rc.camera.get_color_image()

    if image is None:
        contour_center = None
        contour_area = 0
    else:
        # Find all blue and red contours
        contours_blue = rc_utils.find_contours(image, BLUE[0], BLUE[1])

        # Select the largest contour of each color
        contour_blue = rc_utils.get_largest_contour(contours_blue, MIN_CONTOUR_AREA)
        
        #Find the contour area of each color
        blue_area = rc_utils.get_contour_area(contour_blue) if contour_blue is not None else 0.0

        contour = contour_blue

        if contour is not None:
            # Calculate contour information
            contour_blue_center = rc_utils.get_contour_center(contour)
            contour_blue_area = rc_utils.get_contour_area(contour)

            # Draw contour onto the image
            # rc_utils.draw_contour(image, contour)
            # rc_utils.draw_circle(image, contour_blue_center)            
            # rc_utils.draw_circle(image, [contour_center[0], contour_center[1] + OFFSET_DIST])

        else:
            contour_blue_center = None
            contour_blue_area = 0

        return contour
        # Display the image to the screen
        #rc.display.show_color_image(image)

def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    # TODO: Slalom between red and blue cones.  The car should pass to the right of
    # each red cone and the left of each blue cone.

    global angle
    global speed
    
    global contour_red_center
    global contour_blue_center
    global contour_red_area
    global contour_blue_area
    
    global curr_state
    global turning
    global counter
    global offset_dist

    red_contour = update_red_contour()
    blue_contour = update_blue_contour()
    image = rc.camera.get_color_image()
    depth_image_original = rc.camera.get_depth_image()
    red_depth = 0.0
    blue_depth = 0.0

    if curr_state == State.search:
        print("search")
        if red_contour is not None and blue_contour is not None:
            red_depth = depth_image_original[contour_red_center[0]][contour_red_center[1]]
            blue_depth = depth_image_original[contour_blue_center[0]][contour_blue_center[1]]
            
            if red_depth < blue_depth:
                curr_state = State.approach_red
            elif blue_depth < red_depth:
                curr_state = State.approach_blue
        elif red_contour is not None:
            curr_state = State.approach_red
        elif blue_contour is not None:
            curr_state = State.approach_blue
        else:
            speed = 0.5
            angle = -0.75
    
    if curr_state == State.approach_red:
        print("approach_red")
        if red_contour is None:
            curr_state = State.search
        else:
            red_depth = depth_image_original[contour_red_center[0]][contour_red_center[1]]
            if red_depth > dist:
                angle = rc_utils.remap_range(contour_red_center[1], 0, rc.camera.get_width(), -1, 1, True)
                speed = 0.5
            else:
                curr_state = State.dodge_red
    
    if curr_state == State.dodge_red:
        print("dodge_red")
        print(counter)
        counter += rc.get_delta_time()
        if counter < 0.75:
            angle = 1
        elif counter < 1: 
            angle = 0
        elif counter < 1.75: 
            angle = -1
        else:
            counter = 0
            curr_state = State.search
    
    if curr_state == State.approach_blue:
        print("approach_blue")
        if blue_contour is None:
            curr_state = State.search
        else:
            blue_depth = depth_image_original[contour_blue_center[0]][contour_blue_center[1]]
            if blue_depth > dist:
                angle = rc_utils.remap_range(contour_blue_center[1], 0, rc.camera.get_width(), -1, 1, True)
                speed = 0.5
            else:
                curr_state = State.dodge_blue
    
    if curr_state == State.dodge_blue:
        print("dodge_blue")
        counter += rc.get_delta_time()
        if counter < 0.75:
            angle = -1
        elif counter < 1: 
            angle = 0
        elif counter < 1.75: 
            angle = 1
        else:
            counter = 0
            curr_state = State.search
    
    rc.drive.set_speed_angle(speed, angle)

    #Debug
    if rc.controller.is_down(rc.controller.Button.A):
        print(f"State:{curr_state} Speed{speed:.2f} Angle: {angle} Area:")
    if rc.controller.is_down(rc.controller.Button.B):
        print(f"Red depth:{red_depth} Blue depth:{blue_depth}")


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()

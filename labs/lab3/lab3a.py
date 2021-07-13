"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020

Lab 3A - Depth Camera Safety Stop
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

# Add any global variables here

########################################################################################
# Functions
########################################################################################

def crop(
    image,
    top_left_inclusive,
    bottom_right_exclusive
):
    
    # Extract the minimum and maximum pixel rows and columns from the parameters
    r_min, c_min = top_left_inclusive
    r_max, c_max = bottom_right_exclusive
    # Shorten the array to the specified row and column ranges
    return image[r_min:r_max, c_min:c_max]


def start():
    """
    This function is run once every time the start button is pressed
    """
    # Have the car begin at a stop
    rc.drive.stop()

    # Print start message
    print(
        ">> Lab 3A - Depth Camera Safety Stop\n"
        "\n"
        "Controls:\n"
        "    Right trigger = accelerate forward\n"
        "    Right bumper = override safety stop\n"
        "    Left trigger = accelerate backward\n"
        "    Left joystick = turn front wheels\n"
        "    A button = print current speed and angle\n"
        "    B button = print the distance at the center of the depth image"
    )


def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    top_left_inclusive = (0, 0)
    bottom_right_exclusive = (rc.camera.get_height() * 2 //3, rc.camera.get_width())


    # Use the triggers to control the car's speed
    rt = rc.controller.get_trigger(rc.controller.Trigger.RIGHT)
    lt = rc.controller.get_trigger(rc.controller.Trigger.LEFT)
    # Calculate the distance of the object directly in front of the car
    depth_image = rc.camera.get_depth_image()
    floor_distance_pt = rc_utils.get_closest_pixel(depth_image)
    floor_distance = depth_image[floor_distance_pt[0]][floor_distance_pt[1]]

    dist_image = crop(depth_image, top_left_inclusive, bottom_right_exclusive)
    center_distance = rc_utils.get_depth_image_center_distance(dist_image)
    
    
    # TODO (warmup): Prevent forward movement if the car is about to hit something.
    if not rc.controller.is_down(rc.controller.Button.RB) and center_distance < 60 and center_distance != 0.0:
        print('center distance: ' + str(center_distance))
        rt = 0

    print('center distance: ' + str(center_distance))

    # Allow the user to override safety stop by holding the right bumper.

    # Print the current speed and angle when the A button is held down
    if rc.controller.is_down(rc.controller.Button.A):
        print("Speed:", speed, "Angle:", angle)

    # Print the depth image center distance when the B button is held down
    if rc.controller.is_down(rc.controller.Button.B):
        print("Center distance:", center_distance)

    # Display the current depth image
    rc.display.show_depth_image(depth_image)

    # TODO (stretch goal): Prevent forward movement if the car is about to drive off a
    # ledge.  ONLY TEST THIS IN THE SIMULATION, DO NOT TEST THIS WITH A REAL CAR.
    print("Floor Distance" + str(floor_distance))
    if(floor_distance > 50):
       rt = 0
    
    speed = rt - lt 
    # Use the left joystick to control the angle of the front wheels
    angle = rc.controller.get_joystick(rc.controller.Joystick.LEFT)[0]
    rc.drive.set_speed_angle(speed, angle)

########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()

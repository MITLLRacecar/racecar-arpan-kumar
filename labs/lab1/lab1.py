"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020

Lab 1 - Driving in Shapes
"""

########################################################################################
# Imports
########################################################################################

import sys

sys.path.insert(1, "../../library")
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# Put any global variables here
ctr = 0
curr_button = " "
########################################################################################
# Functions
########################################################################################


def start():
    """
    This function is run once every time the start button is pressed
    """
    # Begin at a full stop
    rc.drive.stop()

    # Print start message
    # TODO (main challenge): add a line explaining what the Y button does
    print(
        ">> Lab 1 - Driving in Shapes\n"
        "\n"
        "Controls:\n"
        "    Right trigger = accelerate forward\n"
        "    Left trigger = accelerate backward\n"
        "    Left joystick = turn front wheels\n"
        "    A button = drive in a circle\n"
        "    B button = drive in a square\n"
        "    X button = drive in a figure eight\n"
    )


def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    global ctr
    global curr_button

    ctr += rc.get_delta_time()
        
    rc.drive.set_speed_angle(0, 0)

    if rc.controller.was_pressed(rc.controller.Button.A):
        print("Driving in a circle...")
        curr_button = "a"
        ctr = 0
    elif rc.controller.was_pressed(rc.controller.Button.B):
        print("Driving in a square...")
        curr_button = "b"
        ctr = 0
    elif rc.controller.was_pressed(rc.controller.Button.X):
        print("Driving in a figure eight...")
        curr_button = "x"
        ctr = 0
    elif rc.controller.was_pressed(rc.controller.Button.Y):
        print("Driving in a triangle...")
        curr_button = "y"
        ctr = 0
    elif rc.controller.get_trigger(rc.controller.Trigger.RIGHT) != 0:
        print("right trigger")
        rc.drive.set_speed_angle(1, 0)
    elif rc.controller.get_trigger(rc.controller.Trigger.LEFT) != 0:
        print("left trigger")
        rc.drive.set_speed_angle(-1, 0)
    elif rc.controller.get_joystick(rc.controller.Joystick.LEFT) != 0:
        left_joystick = rc.controller.get_joystick(rc.controller.Joystick.LEFT)
        print("joystick: " + str(left_joystick))
        rc.drive.set_speed_angle(0, left_joystick[0])
    
    if curr_button == "a":
        rc.drive.set_speed_angle(1, 0.5)
    elif curr_button == "b":
        if ctr < 2:
            rc.drive.set_speed_angle(0.5, 0)
        elif ctr < 7:
            rc.drive.set_speed_angle(0.5, 0.5)
        elif ctr < 9:
            rc.drive.set_speed_angle(0.5, 0)
        elif ctr < 14:
            rc.drive.set_speed_angle(0.5, 0.5)
        elif ctr < 16:
            rc.drive.set_speed_angle(0.5, 0)
        elif ctr < 21:
            rc.drive.set_speed_angle(0.5, 0.5)
        elif ctr < 22:
            rc.drive.set_speed_angle(0.5, 0)  
    elif curr_button == "x":
        if ctr < 5:
            rc.drive.set_speed_angle(1, 1)
        elif ctr < 10:
            rc.drive.set_speed_angle(1, -1)
        else:
            ctr = 0
    elif curr_button == "y":
        if ctr < 3:
            rc.drive.set_speed_angle(0.5, 0)
        elif ctr < 7:
            rc.drive.set_speed_angle(0.5, 0.75)
        elif ctr < 10:
            rc.drive.set_speed_angle(0.5, 0)
        elif ctr < 14:
            rc.drive.set_speed_angle(0.5, 0.75)
        elif ctr < 17:
            rc.drive.set_speed_angle(0.5, 0)
        elif ctr < 21:
            rc.drive.set_speed_angle(0.5, 0.75)
        else:
            ctr = 0
    

########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update)
    rc.go()

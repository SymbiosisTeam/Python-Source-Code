# TEAM SYMBIOSIS
# SIT374 - Project Design
# Trimester 1, 2018
# CrazyFlie 2.0 Drone - Flight-Control Solution Prototype

"""
Bitcraze CrazyFlie 2.0 Drone
 - Automatic Flight-Control Prototype Solution

This program connects to the Crazyflie at the `URI` and runs a flight 
sequence to simulate how the drone will operate in the Deakin Motion Capture Lab.

This program does not utilise an external location system: it has been
tested with (and designed for) the Flowdeck in line with our Sprint 2 goals.

"""

import logging
import time
import math

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

URI = 'radio://0/80/250K'

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

"""
ATTENTION: 	
USER TO ENTER VALUES FOR WAYPOINT CO-ORDINATE (X, Y, Z)
"""

# USER-DEFINED CO-ORDINATES
X = 
Y = 
Z = 

# General Attributes - DO NOT MODIFY
initVelocityDrone = 0.5
heightDrone = 0
hoverTime = 120	# seconds
yawRate = 0
velocitySide = 0
climb = True

# Equations - DO NOT MODIFY
angle = math.degrees(math.atan(Y / X))
distance = math.sqrt((X * X + Y * Y))					# Pythagoras Theorem
travelTime = (round)(distance / initVelocityDrone)      # Get time as an integer value
velocityForward = distance / travelTime                 # Recalculate drone velocity to accomodate for time as an integer
			

'''
CrazyFlie Drone Flight Control
'''

# Method: Runs a FOR loop over a set number of iterations to continuously send motion inputs
# 		  to CrazyFlie drone
def RunFlightSequence(iterations, vx, vy, yawRate, z):
	for i in range(iterations):
            cf.commander.send_hover_setpoint(vx, vy, yawRate, z)
            time.sleep(0.1)

# Method: Runs a FOR loop over a set number of iterations to continuously send vertical motion inputs
# 		  to CrazyFlie drone, climbing or descending based on a boolean value
def RunVerticalFlightSequence(iterations, vx, vy, yawRate, climb)
    if climb is True:
	    for i in range(iterations):
            z = i * 0.02
			cf.commander.send_hover_setpoint(vx, vy, yawRate, z)
            time.sleep(0.1)
	else:
	    for i in range(10):
            z = (10 - i) * 0.02
			cf.commander.send_hover_setpoint(vx, vy, yawRate, z)
            time.sleep(0.1)
		    
			
# Flight-Control Program
if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        cf = scf.cf

        cf.param.set_value('kalman.resetEstimation', '1')
        time.sleep(0.1)
        cf.param.set_value('kalman.resetEstimation', '0')
        time.sleep(2)

		'''
		TAKE-OFF
		'''
		# Height = 0.2 metres
		iterations = 10 + 1
		
        # Run Climb Sequence
		RunVerticalFlightSequence(iterations, 0, velocitySide, climb)

		'''
		ROTATE
		'''
		# Rotate to correct orientation
		# Positive YAW is anti-clockwise
		# Set yawTime
		yawTime = 2 	# Two second 
		
		# Calculate yawRate
		yawRate = angle / yawTime
		
		# Calculate Iterations for loop
		iterations = yawTime * 10 + 1
		
		#Run Sequence
		RunFlightSequence(iterations, 0, velocitySide, yawRate, heightDrone)
		
		'''
		TRAVERSE FLIGHT PATH TO DESTINATION WAYPOINT
		'''
		# Fly straight line to designated point (x, y, z)
		# Increase height over distance
		climbRate = (Z - heightDrone) / travelTime
		iterations = travelTime + 1
        
		#Run Sequence
		RunFlightSequence(iterations, velocityForward, velocitySide, 0, climbRate) 
		
		'''
		HOVER AT DESTINATION WAYPOINT
		'''
		# To demonstrate how drone will interact with actor during motion capture
		iterations = hoverDuration * 10
		
		#Run Sequence
		RunFlightSequence(iterations, 0, velocitySide, 0, heightDrone)

		'''
		TRAVERSE FROM WAYPOINT TO ORIGIN
		'''
		# Reverse flight-path
		# Fly straight line to origin (0, 0, 0)
		# Decrease height over distance
		climbRate = (heightDrone - Z) / travelTime
		iterations = travelTime + 1
        
		#Run Sequence
		RunFlightSequence(iterations, -velocityForward, velocitySide, 0, climbRate)
		
		'''
		ROTATE
		'''
		# Rotate to original orientation
		# Negative YAW is clockwise
		# Set yawTime
		yawTime = 2 	# Two seconds
		
		# Calculate yawRate
		yawRate = angle / yawTime
		
		#Calculate Iterations for loop
		iterations = yawTime * 10 + 1
		
		#Run Sequence
		RunFlightSequence(iterations, 0, velocitySide, -yawRate, heightDrone)
        		
		'''
		LAND and SHUTDOWN
		'''
		# Descend to 0 metres
		
		# Run Descend Sequence
		climb = False
		RunVerticalFlightSequence(iterations, 0, velocitySide, climb)
  		
		# Engine shut-off
        cf.commander.send_stop_setpoint()
